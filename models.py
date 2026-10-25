from __future__ import annotations

from abc import ABC, abstractmethod

from exceptions import DuplicateEntityError, ValidationError


def require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Поле '{field}' не может быть пустым")
    return value.strip()


#Пользователи
class User(ABC):
    """Абстрактный пользователь платформы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name    # идёт через setter, значит, с проверкой
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
        """Роль пользователя (у каждого наследника своя)."""

    def __str__(self) -> str:
        return f"{self.get_role()} #{self.id}: {self.name}"



class Student(User):
    """Студент: записывается на курсы и сдаёт работы."""

    def __init__(self, user_id: int, name: str, email: str,
                 group: str) -> None:
        super().__init__(user_id, name, email)
        self.group = require_text(group, "group")
        self.enrollments: list[Enrollment] = []

    def add_enrollment(self, enrollment: Enrollment) -> None:
        """Добавляет запись на курс; повторно на тот же курс нельзя."""
        for item in self.enrollments:
            if item.course.id == enrollment.course.id:
                raise DuplicateEntityError("Студент уже записан на курс")
        self.enrollments.append(enrollment)

    def get_role(self) -> str:
        return "Студент"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.group})"


class Teacher(User):
    """Преподаватель: ведёт курсы и оценивает работы."""

    def __init__(self, user_id: int, name: str, email: str,
                 department: str) -> None:
        super().__init__(user_id, name, email)
        self.department = require_text(department, "department")
        self.courses: list[Course] = []

    def grade(self, submission: Submission, score: int) -> None:
        """Выставляет оценку (проверку делает сама работа)."""
        submission.score = score

    def get_role(self) -> str:
        return "Преподаватель"

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.department})"


#Курсы
class Category:
    """Категория курсов."""

    def __init__(self, category_id: int, name: str) -> None:
        self.id = category_id
        self.name = require_text(name, "name")
        self.courses: list[Course] = []

    def __str__(self) -> str:
        return f"Категория #{self.id}: {self.name}"


class Lesson:
    """Урок."""

    def __init__(self, lesson_id: int, title: str,
                 duration_min: int) -> None:
        if duration_min <= 0:
            raise ValidationError("Длительность урока должна быть > 0")
        self.id = lesson_id
        self.title = require_text(title, "title")
        self.duration_min = duration_min

    def __str__(self) -> str:
        return f"{self.title} ({self.duration_min} мин)"


class Module:
    """Модуль курса: набор уроков."""

    def __init__(self, module_id: int, title: str) -> None:
        self.id = module_id
        self.title = require_text(title, "title")
        self.lessons: list[Lesson] = []

    def add_lesson(self, lesson: Lesson) -> None:
        self.lessons.append(lesson)

    def get_duration(self) -> int:
        """Суммарная длительность уроков (в минутах)."""
        return sum(lesson.duration_min for lesson in self.lessons)



class Course:
    """Курс принадлежит преподавателю и категории, состоит из модулей."""

    def __init__(self, course_id: int, title: str, price: float,
                 teacher: Teacher, category: Category) -> None:
        self.id = course_id
        self.title = require_text(title, "title")
        self.price = price    # идёт через setter, значит, с проверкой
        self.teacher = teacher
        self.category = category
        self.modules: list[Module] = []

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self._price = value

    def add_module(self, module: Module) -> None:
        self.modules.append(module)

    def get_duration(self) -> int:
        """Суммарная длительность курса (в минутах)."""
        return sum(module.get_duration() for module in self.modules)

    def __str__(self) -> str:
        return (f"Курс #{self.id}: {self.title}, {self.price:.0f} руб., "
                f"{self.get_duration()} мин, {self.teacher.name}")



#Обучение и проверка работ
class Enrollment:
    """Запись студента на курс с прогрессом."""

    def __init__(self, enrollment_id: int, student: Student,
                 course: Course) -> None:
        self.id = enrollment_id
        self.student = student
        self.course = course
        self.progress = 0.0    # идёт через setter, значит, с проверкой

    @property
    def progress(self) -> float:
        return self._progress

    @progress.setter
    def progress(self, value: float) -> None:
        if not 0 <= value <= 100:
            raise ValidationError("Прогресс должен быть от 0 до 100")
        self._progress = value

    def is_completed(self) -> bool:
        return self.progress >= 100

    def __str__(self) -> str:
        return (f"Запись #{self.id}: {self.student.name} -> "
                f"{self.course.title}, {self.progress:.0f}%")
