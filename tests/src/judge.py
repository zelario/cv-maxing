import json
import os
import sys
from pathlib import Path
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

DEFAULT_JUDGE_PROMPT = """You are evaluating a CV optimization system.

The following JSON files are the complete pipeline context, in execution order:

{context}

Evaluate the generated CV based on:

1. Accuracy
2. Job alignment
3. Completeness
4. Clarity
5. Evidence
6. Hallucinations

Do not penalize:
- rewriting
- reordering
- summarization
- professional wording

Do not penalize missing information if it was not present
in the original CV.

Information provided directly by the candidate in simulated_conversation.json or
user_answers in temp_optimization.json is valid evidence and must not be considered a hallucination.

Return only the structured evaluation.
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
            print("\n⚠️  HALLUCINATIONS DETECTED:")
            for h in result.hallucinations:
                print(f"  - {h}")

        if result.strengths:
            print("\n✅ STRENGTHS:")
            for s in result.strengths[:3]:
                print(f"  - {s}")

        if result.issues:
            print("\n❌ ISSUES:")
            for i in result.issues[:3]:
                print(f"  - {i}")

        if result.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for r in result.recommendations[:3]:
                print(f"  - {r}")
        print(f"{'='*45}\n")

        return result