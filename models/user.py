from __future__ import annotations

from abc import ABC, abstractmethod
from .validation import require_text
from exceptions.validation_error import ValidationError


class User(ABC):
    """Абстрактный пользователь платформы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
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
        """Возвращает роль пользователя."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.get_role()} #{self.id}: {self.name}"

