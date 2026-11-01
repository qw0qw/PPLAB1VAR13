from .validation import require_text
from exceptions.validation_error import ValidationError


class Submission:
    """Работа студента по заданию."""

    def __init__(self, submission_id: int, student: "Student",
                 assignment: "Assignment", text: str) -> None:
        self.id = submission_id
        self.student = student
        self.assignment = assignment
        self.text = require_text(text, "text")
        self._score: int | None = None

    @property
    def score(self) -> int | None:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if not 0 <= value <= self.assignment.max_score:
            raise ValidationError(
                f"Оценка должна быть от 0 до {self.assignment.max_score}")
        self._score = value

    def __str__(self) -> str:
        return (f"Работа #{self.id}: {self.student.name}, "
                f"{self.assignment.title}, оценка: {self.score}")
