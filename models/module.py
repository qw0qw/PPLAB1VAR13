from .validation import require_text


class Module:
    """Модуль курса: набор уроков."""

    def __init__(self, module_id: int, title: str) -> None:
        self.id = module_id
        self.title = require_text(title, "title")
        self.lessons = []

    def add_lesson(self, lesson: "Lesson") -> None:
        self.lessons.append(lesson)

    def get_duration(self) -> int:
        """Возвращает суммарную длительность уроков в минутах."""
        return sum(lesson.duration_min for lesson in self.lessons)
