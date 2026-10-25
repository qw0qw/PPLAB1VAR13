"""Универсальное хранилище с базовыми CRUD операциями."""
from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from exceptions import DuplicateEntityError, EntityNotFoundError


class HasId(Protocol):
    """Любой объект, у которого есть числовой id."""

    id: int


T = TypeVar("T", bound=HasId)


class Repository(Generic[T]):
    """Хранит объекты одного типа в словаре {id: объект}."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._items: dict[int, T] = {}

    def create(self, item: T) -> T:
        """Create: добавляет объект, id должен быть уникальным."""
        if item.id in self._items:
            raise DuplicateEntityError(
                f"{self._name} с id={item.id} уже существует")
        self._items[item.id] = item
        return item

    def get(self, item_id: int) -> T:
        """Read: возвращает объект по id."""
        if item_id not in self._items:
            raise EntityNotFoundError(
                f"{self._name} с id={item_id} не найден")
        return self._items[item_id]

    def get_all(self) -> list[T]:
        """Read: возвращает все объекты."""
        return list(self._items.values())

    def update(self, item: T) -> None:
        """Update: заменяет существующий объект."""
        self.get(item.id)    # бросит EntityNotFoundError, если нет
        self._items[item.id] = item

    def delete(self, item_id: int) -> None:
        """Delete: удаляет объект по id."""
        self.get(item_id)
        del self._items[item_id]
