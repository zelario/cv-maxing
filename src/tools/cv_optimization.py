from threading import Lock
from typing import Callable

from crewai.tools import tool

_handler_lock = Lock()
_question_handler: Callable[[str], str] | None = None


def set_question_handler(handler: Callable[[str], str] | None) -> None:
    """Attach the current web session's question handler to the agent tool."""

    global _question_handler
    with _handler_lock:
        _question_handler = handler


@tool("ask_user")
def ask_user(question: str) -> str:
    """Ask through the web session, or prompt in the terminal for CLI runs."""

    with _handler_lock:
        handler = _question_handler
    if handler is None:
        print(f"\n[CV MAXING QUESTION] {question}")
        return input("Your answer (or press Enter to skip): ").strip()
    return handler(question)
