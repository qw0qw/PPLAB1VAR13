"""Базовая реализация универсального репозитория."""
from __future__ import annotations

from typing import Generic, TypeVar

from exceptions.duplicate_entity_error import DuplicateEntityError
from exceptions.entity_not_found_error import EntityNotFoundError
from .interfaces import HasId

T = TypeVar("T", bound=HasId)

class Repository(Generic[T]):
    """Хранит объекты одного типа в словаре {id: объект}."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._items: dict[int, T] = {}

    def create(self, item: T) -> T:
        """Добавляет объект; id должен быть уникальным."""
        if item.id in self._items:
            raise DuplicateEntityError(
                f"{self._name} с id={item.id} уже существует"
            )
        self._items[item.id] = item
        return item

    def get(self, item_id: int) -> T:
        """Возвращает объект по id."""
        if item_id not in self._items:
            raise EntityNotFoundError(
                f"{self._name} с id={item_id} не найден"
            )
        return self._items[item_id]

    def get_all(self) -> list[T]:
        """Возвращает список всех объектов."""
        return list(self._items.values())

    def update(self, item: T) -> None:
        """Заменяет существующий объект."""
        self.get(item.id)
        self._items[item.id] = item

    def delete(self, item_id: int) -> None:
        """Удаляет объект по id."""
        self.get(item_id)
        del self._items[item_id]
