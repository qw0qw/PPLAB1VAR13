"""Протоколы, описывающие требования к объектам репозитория."""
from typing import Protocol

class HasId(Protocol):
    """Любой объект, у которого есть числовой id."""
    id: int
