import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from google import genai
from google.genai import types

TESTS_SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_SRC_DIR.parents[1]
TEMP_DIR = PROJECT_ROOT / "temp"

sys.path.insert(0, str(TESTS_SRC_DIR))

try:
    from models.validation import ValidationResult
except ImportError:
    from tests.src.models.validation import ValidationResult

DEFAULT_JUDGE_PROMPT = """You are an expert Human-Centered AI (HCAI) evaluator assessing the output of a CV tailoring pipeline.

The following JSON files represent the complete pipeline execution context, in execution order:

{context}

GROUND TRUTH SOURCE OF EVIDENCE:
- Valid evidence includes: (1) facts explicitly stated in temp_cv.json, and (2) information confirmed or provided directly by the candidate in simulated_conversation.json (or user_provided_evidence in temp_optimization.json).
- Rewriting, reordering, professional styling, and synthesizing concise summaries from verified facts are expected and must NOT be penalized.
- Do NOT penalize missing information if it was neither present in the original CV nor provided by the candidate.

EVALUATION RUBRIC (Score 0 to 10 for each dimension):

1. Accuracy (0-10):
   - Definition: Strict factual truthfulness against candidate evidence. Are job titles, employers, dates, degrees, grades, technologies, and metrics completely faithful?
   - 10: Flawless factual fidelity. Zero fabricated facts.
   - 8-9: Benign professional wording that remains completely true to verified candidate capabilities.
   - 5-7: Unevidenced minor metrics or tools present without candidate confirmation.
   - 0-4: Clear fabrication of experience, degrees, fake employers, or claiming skills the candidate explicitly stated they do NOT possess.
   * STRICT RULE: If the hallucinations list contains any items, accuracy_score MUST NOT exceed 6.

2. Job Alignment (0-10):
   - Definition: How effectively the CV tailors, emphasizes, and structures verified candidate background to align with the target job requirements (temp_job.json).
   - 9-10: Excellent alignment. Relevant verified skills, projects, and experiences are prominent and directly targeted to the role.
   - 6-8: Moderate alignment. The CV aligns with several requirements, though natural gaps exist in the candidate's background.
   - 1-5: Low alignment due to a natural mismatch between the candidate's domain and the job (e.g. pure Frontend applying to Data Science, or Doctor applying to IT). Note: Reflect candidate-job discrepancy factually; do not penalize the system if the candidate simply lacks those skills.

3. Completeness (0-10):
   - Definition: Structural coverage of standard CV sections (Header, Contact Info, Links, Professional Summary, Experience, Education, Skills, Languages, Certifications, Projects, and GDPR Consent) and integration of candidate-provided details.
   - 10: All applicable sections are present, well-populated, and integrate all user-provided details (links, email, phone, certifications, languages).
   - 8-9: Core sections present; minor optional elements omitted.
   - 0-7: Missing essential sections (e.g., missing contact info, missing experience, or missing education).

4. Clarity (0-10):
   - Definition: Readability, professional tone, grammar, and clean information hierarchy.
   - 9-10: Professional executive tone, clean action-verb bullet points, clear skill categorization, and crisp summary.
   - 7-8: Readable and clear, with minor wordiness or generic phrasing.
   - 0-6: Disorganized, repetitive phrasing, awkward grammar, or confusing layout.

5. Evidence (0-10):
   - Definition: Grounding of skills and claims in demonstrable context (roles, projects, courses, metrics) rather than unsupported buzzwords.
   - 9-10: Every listed technical skill and capability is substantiated by context in experience, education, or projects.
   - 7-8: Most skills are grounded; a few appear as standalone items without narrative context.
   - 0-6: Pervasive buzzword stuffing with little or no supporting context.

6. Hallucinations (list[str]):
   - Explicitly list any skill, technology, certification, metric, employer, degree, or responsibility claimed in temp_generated_cv.json that has NO basis in temp_cv.json AND was NOT provided by the candidate in simulated_conversation.json.
   - Crucially: If the candidate explicitly stated "I do not have experience with X" and X appears in the generated CV, flag it here.
   - If no hallucinations exist, return an empty list [].

7. Qualitative Feedback:
   - strengths: Concrete positive aspects of the generated CV.
   - issues: Specific weaknesses, unfulfilled requirements, or evidence gaps.
   - recommendations: Actionable advice for the candidate to improve their fit.

Return ONLY the structured evaluation adhering to the schema.
"""


class Judge:
    PIPELINE_FILES = (
        "temp_cv.json",
        "temp_job.json",
        "temp_review.json",
        "temp_optimization.json",
        "temp_generated_cv.json",
    )

    def __init__(self, model: str, prompt_template: str | None = None):
        api_key = os.getenv("GEMINI_VALIDATION_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.model = model
        self.prompt_template = prompt_template

    def evaluate(self, directory: Path | None = None) -> ValidationResult | None:
        """Loads pipeline JSON files from temp/, evaluates with Judge LLM, and prints report."""
        target_dir = directory or TEMP_DIR

        # 1. Load pipeline outputs
        outputs = []
        for filename in self.PIPELINE_FILES:
            path = target_dir / filename
            if not path.is_file():
                print(f"[JUDGE ERROR] Missing required pipeline output: {path}")
                return None
            outputs.append(f"{filename}:\n{path.read_text(encoding='utf-8')}")

        conv_path = target_dir / "simulated_conversation.json"
        if conv_path.is_file():
            outputs.append(f"simulated_conversation.json:\n{conv_path.read_text(encoding='utf-8')}")

        context = "\n\n".join(outputs)
        template = self.prompt_template or DEFAULT_JUDGE_PROMPT
        prompt = template.format(context=context) if "{context}" in template else f"{template}\n\n{context}"

        # 2. Query Judge LLM
        print(f"\n[JUDGE] Evaluating outputs in {target_dir} with {self.model}...")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ValidationResult,
                ),
            )
        except Exception as exc:
            print(f"\n[FATAL API ERROR] Judge API/model error ({self.model}): {exc}")
            print("[FATAL API ERROR] Terminating execution immediately as configured.\n")
            sys.exit(1)

        if not response.text and not response.parsed:
            print(f"\n[FATAL API ERROR] Judge received an empty response from LLM ({self.model}).")
            sys.exit(1)

        result = (
            ValidationResult.model_validate_json(response.text)
            if response.text
            else response.parsed
        )

        # 3. Save result JSON
        (target_dir / "temp_judge.json").write_text(
            result.model_dump_json(indent=2) + "\n", encoding="utf-8"
        )

        # 4. Print clean scores report
        print(f"\n{'='*45}\n               JUDGE SCORES\n{'='*45}")
        print(f"  Accuracy:       {result.accuracy_score}/10")
        print(f"  Job Alignment:  {result.job_alignment_score}/10")
        print(f"  Completeness:   {result.completeness_score}/10")
        print(f"  Clarity:        {result.clarity_score}/10")
        print(f"  Evidence:       {result.evidence_score}/10")

        if result.hallucinations:
            print("\n[!] HALLUCINATIONS DETECTED:")
            for h in result.hallucinations:
                print(f"  - {h}")

        if result.strengths:
            print("\n[+] STRENGTHS:")
            for s in result.strengths[:3]:
                print(f"  - {s}")

        if result.issues:
            print("\n[-] ISSUES:")
            for i in result.issues[:3]:
                print(f"  - {i}")

        if result.recommendations:
            print("\n[*] RECOMMENDATIONS:")
            for r in result.recommendations[:3]:
                print(f"  - {r}")
        print(f"{'='*45}\n")

        return result
