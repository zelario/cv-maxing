import io
from pathlib import Path

import pdfplumber
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from models.generated_cv import GeneratedCV

HTML_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv.html"
CSS_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv.css"


def render_cv_html(generated: GeneratedCV) -> str:
    """Render generated CV data with the reusable HTML/CSS design template."""

    model = GeneratedCV.model_validate(generated.model_dump())
    env = Environment(
        loader=FileSystemLoader(str(HTML_TEMPLATE_PATH.parent)),
        autoescape=True,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = env.get_template(HTML_TEMPLATE_PATH.name)
    html = template.render(**model.model_dump())
    css = CSS_TEMPLATE_PATH.read_text(encoding="utf-8")
    return html.replace("</head>", f"<style>\n{css}\n</style>\n</head>")


def render_cv_pdf(html: str) -> bytes:
    """Render a CV HTML document as an A4 PDF using Chromium with bottom-anchored GDPR consent."""

    with sync_playwright() as playwright:
        browser = None
        try:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_content(html, wait_until="load")
            pdf_bytes = page.pdf(
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )

            # Anchor GDPR consent statement to the bottom of the page where it is located
            try:
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as doc:
                    if doc.pages:
                        last_page = doc.pages[-1]
                        page_height = float(last_page.height)
                        gdpr_words = [
                            w
                            for w in last_page.extract_words()
                            if "gdpr" in w["text"].lower() or "consent" in w["text"].lower()
                        ]
                        if gdpr_words:
                            current_bottom = max(float(w["bottom"]) for w in gdpr_words)
                            # Target bottom: page_height minus bottom margin (1.76cm in pt) minus safety buffer (15pt)
                            target_bottom = page_height - (1.76 * 72.0 / 2.54) - 15.0
                            delta_pt = target_bottom - current_bottom
                            if delta_pt > 5.0:
                                page.evaluate(
                                    f"""() => {{
                                        const consent = document.querySelector('.consent');
                                        if (consent) {{
                                            const cur = parseFloat(window.getComputedStyle(consent).marginTop) || 0;
                                            consent.style.marginTop = (cur + {delta_pt}) + 'pt';
                                        }}
                                    }}"""
                                )
                                adjusted_pdf_bytes = page.pdf(
                                    format="A4",
                                    print_background=True,
                                    prefer_css_page_size=True,
                                )
                                with pdfplumber.open(io.BytesIO(adjusted_pdf_bytes)) as adj_doc:
                                    if len(adj_doc.pages) == len(doc.pages):
                                        pdf_bytes = adjusted_pdf_bytes
            except Exception:
                pass

            return pdf_bytes
        except PlaywrightError as exc:
            raise RuntimeError(
                "Could not render the CV PDF. Install Playwright's Chromium with "
                "`python -m playwright install chromium`."
            ) from exc
        finally:
            if browser is not None:
                browser.close()
