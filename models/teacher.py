from __future__ import annotations

from .user import User
from .validation import require_text


class Teacher(User):
    """Преподаватель: ведёт курсы и оценивает работы."""

    def __init__(self, user_id: int, name: str, email: str, department: str) -> None:
        super().__init__(user_id, name, email)
        self.department = require_text(department, "department")
        self.courses = []

    def grade(self, submission: "Submission", score: int) -> None:
        """Выставляет оценку работе."""
        submission.score = score

    def get_role(self) -> str:
        return "Преподаватель"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.department})"
