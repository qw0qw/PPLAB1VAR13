from .validation import require_text
from exceptions.validation_error import ValidationError


class Course:
    """Курс принадлежит преподавателю и категории, состоит из модулей."""

    def __init__(self, course_id: int, title: str, price: float,
                 teacher: "Teacher", category: "Category") -> None:
        self.id = course_id
        self.title = require_text(title, "title")
        self.price = price
        self.teacher = teacher
        self.category = category
        self.modules = []

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self._price = value

    def add_module(self, module: "Module") -> None:
        self.modules.append(module)

    def get_duration(self) -> int:
        """Возвращает суммарную длительность курса в минутах."""
        return sum(module.get_duration() for module in self.modules)

    def __str__(self) -> str:
        return (f"Курс #{self.id}: {self.title}, {self.price:.0f} руб., "
                f"{self.get_duration()} мин, {self.teacher.name}")
