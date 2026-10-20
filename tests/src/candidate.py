import os
import sys
from pathlib import Path
from google import genai

TESTS_SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_SRC_DIR))

DEFAULT_CANDIDATE_PROMPT = """You are a job candidate interacting with an AI CV optimization assistant.
The assistant is tailoring your CV for a specific job application.

<YOUR_CURRENT_CV>
{cv}
</YOUR_CURRENT_CV>

<YOUR_ADDITIONAL_FACTUAL_BACKGROUND>
{extra_context}
</YOUR_ADDITIONAL_FACTUAL_BACKGROUND>

<TARGET_JOB_DESCRIPTION>
{job}
</TARGET_JOB_DESCRIPTION>

The assistant has asked you this question:
"{question}"

Instructions:
1. Answer concisely (1 to 2 sentences) in the first person ("I...", "My...").
2. Stay strictly truthful to your CV and your factual background.
3. If the question asks for links (e.g. GitHub, LinkedIn, portfolio) or specific skills/certifications:
   - Provide them ONLY IF they are present in your CV or Additional Factual Background.
   - If they are NOT in your CV or Additional Factual Background, or if your background explicitly states you do not have them, state clearly: "I do not have one" or "I do not have experience with that."
4. NEVER invent or extrapolate skills, technologies, certifications, or past jobs that are not in your background.
5. Do NOT break character or explain that you are an AI. Answer directly as the human job applicant.
"""


class Candidate:
    """Simulates a human candidate answering questions during CV optimization using their CV and extra context."""

    def __init__(
        self,
        cv_text: str,
        job_text: str,
        extra_context: str = "",
        model: str = "gemini-3.5-flash-lite",
        prompt_template: str | None = None,
    ):
        self.cv_text = cv_text
        self.job_text = job_text
        self.extra_context = (
            extra_context.strip() or "No additional background provided beyond the CV."
        )
        self.model = model
        self.prompt_template = prompt_template or DEFAULT_CANDIDATE_PROMPT
        api_key = os.getenv("GEMINI_VALIDATION_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.conversation: list[dict[str, str]] = []

    def answer_question(self, question: str) -> str:
        prompt = self.prompt_template.format(
            cv=self.cv_text,
            extra_context=self.extra_context,
            job=self.job_text,
            question=question,
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            answer = (response.text or "").strip()
            if not answer:
                answer = "I do not have additional information to add."
        except Exception as exc:
            print(f"\n[FATAL API ERROR] Erro na API/modelo ({self.model}): {exc}")
            print("[FATAL API ERROR] A terminar a execução imediatamente conforme configurado.\n")
            sys.exit(1)

        print(f"\n[CANDIDATE QUESTION] {question}")
        print(f"[CANDIDATE ANSWER]   {answer}\n")

        self.conversation.append({"question": question, "answer": answer})
        return answer
