from __future__ import annotations

from abc import ABC, abstractmethod

from exceptions import DuplicateEntityError, ValidationError


def require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Поле '{field}' не может быть пустым")
    return value.strip()


#Пользователи
class User(ABC):
    """Абстрактный пользователь платформы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name    # идёт через setter, значит, с проверкой
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = require_text(value, "name")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        value = require_text(value, "email")
        if "@" not in value:
            raise ValidationError("Некорректный email")
        self._email = value

    @abstractmethod
    def get_role(self) -> str:
        """Роль пользователя (у каждого наследника своя)."""

    def __str__(self) -> str:
        return f"{self.get_role()} #{self.id}: {self.name}"



class Student(User):
    """Студент: записывается на курсы и сдаёт работы."""

    def __init__(self, user_id: int, name: str, email: str,
                 group: str) -> None:
        super().__init__(user_id, name, email)
        self.group = require_text(group, "group")
        self.enrollments: list[Enrollment] = []

    def add_enrollment(self, enrollment: Enrollment) -> None:
        """Добавляет запись на курс; повторно на тот же курс нельзя."""
        for item in self.enrollments:
            if item.course.id == enrollment.course.id:
                raise DuplicateEntityError("Студент уже записан на курс")
        self.enrollments.append(enrollment)

    def get_role(self) -> str:
        return "Студент"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.group})"


class Teacher(User):
    """Преподаватель: ведёт курсы и оценивает работы."""

    def __init__(self, user_id: int, name: str, email: str,
                 department: str) -> None:
        super().__init__(user_id, name, email)
        self.department = require_text(department, "department")
        self.courses: list[Course] = []

    def grade(self, submission: Submission, score: int) -> None:
        """Выставляет оценку (проверку делает сама работа)."""
        submission.score = score

    def get_role(self) -> str:
        return "Преподаватель"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.department})"
