from .validation import require_text
from exceptions.validation_error import ValidationError


class Lesson:
    """Урок."""

    def __init__(self, lesson_id: int, title: str, duration_min: int) -> None:
        if duration_min <= 0:
            raise ValidationError("Длительность урока должна быть > 0")
        self.id = lesson_id
        self.title = require_text(title, "title")
        self.duration_min = duration_min

    def __str__(self) -> str:
        return f"{self.title} ({self.duration_min} мин)"
