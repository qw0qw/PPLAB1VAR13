"""Публичный интерфейс пакета репозиториев."""
from .interfaces import HasId
from .base import Repository

__all__ = ["HasId", "Repository"]
