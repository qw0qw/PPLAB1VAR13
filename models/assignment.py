from .validation import require_text
from exceptions.validation_error import ValidationError


class Assignment:
    """Задание."""

    def __init__(self, assignment_id: int, title: str, max_score: int) -> None:
        if max_score <= 0:
            raise ValidationError("Максимальный балл должен быть > 0")
        self.id = assignment_id
        self.title = require_text(title, "title")
        self.max_score = max_score

    def __str__(self) -> str:
        return f"Задание #{self.id}: {self.title} (макс. {self.max_score})"
