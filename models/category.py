from .validation import require_text


class Category:
    """Категория курсов."""

    def __init__(self, category_id: int, name: str) -> None:
        self.id = category_id
        self.name = require_text(name, "name")
        self.courses = []

    def __str__(self) -> str:
        return f"Категория #{self.id}: {self.name}"
