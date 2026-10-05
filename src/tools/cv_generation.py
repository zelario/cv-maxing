from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from models.generated_cv import GeneratedCV

MARKDOWN_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv_template.md.j2"
HTML_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv.html"
CSS_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv.css"


def render_cv_markdown(generated: GeneratedCV) -> str:
    """Render the fixed Jinja2 template without adding candidate data."""

    model = GeneratedCV.model_validate(generated.model_dump())

    env = Environment(
        loader=FileSystemLoader(str(MARKDOWN_TEMPLATE_PATH.parent)),
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    return env.get_template(MARKDOWN_TEMPLATE_PATH.name).render(**model.model_dump())


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
    """Render a CV HTML document as an A4 PDF using Chromium."""

    with sync_playwright() as playwright:
        browser = None
        try:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_content(html, wait_until="load")
            return page.pdf(
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )
        except PlaywrightError as exc:
            raise RuntimeError(
                "Could not render the CV PDF. Install Playwright's Chromium with "
                "`python -m playwright install chromium`."
            ) from exc
        finally:
            if browser is not None:
                browser.close()
