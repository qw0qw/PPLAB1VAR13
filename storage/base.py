"""Базовый интерфейс файлового хранилища."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from learning_platform import LearningPlatform


class Storage(ABC):
    """Абстрактное файловое хранилище."""

    def __init__(self, path: str) -> None:
        self._path = path

    @abstractmethod
    def save(self, platform: LearningPlatform) -> None:
        """Записывает данные платформы в файл."""

    @abstractmethod
    def load(self) -> LearningPlatform:
        """Читает файл и возвращает платформу."""
