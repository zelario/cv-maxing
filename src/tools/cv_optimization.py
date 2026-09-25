from crewai.tools import tool


@tool("ask_user")
def ask_user(question: str) -> str:
    """
    Ask the candidate one focused question and return the answer.
    """

    print(f"[OPTIMIZER QUESTION] {question}")
    return input("Answer: ").strip()

