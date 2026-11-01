from __future__ import annotations

from .user import User
from .validation import require_text
from exceptions.duplicate_entity_error import DuplicateEntityError


class Student(User):
    """Студент: записывается на курсы и сдаёт работы."""

    def __init__(self, user_id: int, name: str, email: str, group: str) -> None:
        super().__init__(user_id, name, email)
        self.group = require_text(group, "group")
        self.enrollments = []

    def add_enrollment(self, enrollment: "Enrollment") -> None:
        """Добавляет запись на курс; повторная запись на тот же курс запрещена."""
        for item in self.enrollments:
            if item.course.id == enrollment.course.id:
                raise DuplicateEntityError("Студент уже записан на курс")
        self.enrollments.append(enrollment)

    def get_role(self) -> str:
        return "Студент"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.group})"
