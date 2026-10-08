from google import genai
from models.validation import ValidationResult


class Judge:
    def __init__(self, model: str):
        self.client = genai.Client()
        self.model = model

    def evaluate(
        self,
        pipeline_outputs: list[tuple[str, dict]],
    ) -> ValidationResult:
        context = "\n\n".join(
            f"{filename}:\n{content}" for filename, content in pipeline_outputs
        )

        prompt = f"""
You are evaluating a CV optimization system.

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

Return only the structured evaluation.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ValidationResult,
            },
        )

        return response.parsed