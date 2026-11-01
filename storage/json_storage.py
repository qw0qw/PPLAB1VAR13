"""Реализация файлового хранилища JSON."""
import json

from exceptions.storage_error import StorageError
from .base import Storage
from .serialization import platform_to_dict, restore_platform


class JsonStorage(Storage):
    """Хранилище в формате JSON."""

    def save(self, platform) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                json.dump(platform_to_dict(platform), file,
                          ensure_ascii=False, indent=2)
        except OSError as error:
            raise StorageError(f"Не удалось записать файл: {error}") from error

    def load(self):
        try:
            with open(self._path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise StorageError(f"Файл {self._path} не найден") from None
        except (OSError, ValueError) as error:
            raise StorageError(f"Не удалось прочитать файл: {error}") from error
        return restore_platform(data)
