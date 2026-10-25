from __future__ import annotations

from typing import Callable

from exceptions import LearningError, ValidationError
from learning_platform import LearningPlatform
from models import (
    Assignment,
    Category,
    Course,
    Lesson,
    Module,
    Student,
    Teacher,
)
from storage import JsonStorage, Storage, XmlStorage

# Формат (класс хранилища, имя файла)
STORAGES: dict[str, tuple[type[Storage], str]] = {
    "1": (JsonStorage, "data.json"),
    "2": (XmlStorage, "data.xml"),
}


# Ввод: повторяем вопрос, пока пользователь не введёт верно
def ask_text(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число.")


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Нужно ввести число.")


class ConsoleApp:
    """Меню: каждый пункт - отдельный метод."""

    def __init__(self) -> None:
        self._p = LearningPlatform()
        self._menu: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Добавить преподавателя", self.add_teacher),
            "2": ("Добавить студента", self.add_student),
            "3": ("Добавить категорию", self.add_category),
            "4": ("Добавить курс", self.add_course),
            "5": ("Добавить модуль с уроком в курс", self.add_module),
            "6": ("Записать студента на курс", self.enroll),
            "7": ("Обновить прогресс по курсу", self.update_progress),
            "8": ("Выдать сертификат", self.issue_certificate),
            "9": ("Добавить задание", self.add_assignment),
            "10": ("Сдать работу", self.submit_work),
            "11": ("Оценить работу", self.grade_work),
            "12": ("Показать все данные", self.show_all),
            "13": ("Изменить цену курса", self.change_price),
            "14": ("Удалить курс", self.delete_course),
            "15": ("Сохранить в файл", self.save),
            "16": ("Загрузить из файла", self.load),
        }

    # Create
    def add_teacher(self) -> None:
        teacher = Teacher(self._p.next_id(self._p.teachers),
                          ask_text("Имя: "), ask_text("Email: "),
                          ask_text("Кафедра: "))
        print(f"Добавлен: {self._p.teachers.create(teacher)}")

    def add_student(self) -> None:
        student = Student(self._p.next_id(self._p.students),
                          ask_text("Имя: "), ask_text("Email: "),
                          ask_text("Группа: "))
        print(f"Добавлен: {self._p.students.create(student)}")

    def add_category(self) -> None:
        category = Category(self._p.next_id(self._p.categories),
                            ask_text("Название: "))
        print(f"Добавлена: {self._p.categories.create(category)}")

    def add_course(self) -> None:
        teacher = self._p.teachers.get(ask_int("id преподавателя: "))
        category = self._p.categories.get(ask_int("id категории: "))
        course = Course(self._p.next_id(self._p.courses),
                        ask_text("Название: "), ask_float("Цена: "),
                        teacher, category)
        self._p.courses.create(course)
        teacher.courses.append(course)
        category.courses.append(course)
        print(f"Добавлен: {course}")

    def add_module(self) -> None:
        course = self._p.courses.get(ask_int("id курса: "))
        module = Module(len(course.modules) + 1, ask_text("Модуль: "))
        module.add_lesson(Lesson(1, ask_text("Урок: "),
                                  ask_int("Длительность (мин): ")))
        course.add_module(module)
        print(f"Добавлено. Теперь: {course}")

    def enroll(self) -> None:
        enrollment = self._p.enroll(ask_int("id студента: "),
                                    ask_int("id курса: "))
        print(f"Создано: {enrollment}")

    def add_assignment(self) -> None:
        assignment = Assignment(self._p.next_id(self._p.assignments),
                                ask_text("Название: "),
                                ask_int("Максимальный балл: "))
        print(f"Добавлено: {self._p.assignments.create(assignment)}")

    def submit_work(self) -> None:
        submission = self._p.submit_work(ask_int("id студента: "),
                                         ask_int("id задания: "),
                                         ask_text("Текст работы: "))
        print(f"Сдано: {submission}")

    # Read
    def show_all(self) -> None:
        p = self._p
        sections = [
            ("Преподаватели", p.teachers), ("Студенты", p.students),
            ("Категории", p.categories), ("Курсы", p.courses),
            ("Записи", p.enrollments), ("Задания", p.assignments),
            ("Работы", p.submissions), ("Сертификаты", p.certificates),
        ]
        for title, repo in sections:
            print(f"\n--- {title} ---")
            for item in repo.get_all():
                print(item)

    # Update
    def update_progress(self) -> None:
        enrollment = self._p.enrollments.get(ask_int("id записи: "))
        enrollment.progress = ask_float("Прогресс (0-100): ")
        self._p.enrollments.update(enrollment)
        print(f"Обновлено: {enrollment}")

    def issue_certificate(self) -> None:
        print(self._p.issue_certificate(ask_int("id записи: ")))

    def grade_work(self) -> None:
        self._p.grade_work(ask_int("id преподавателя: "),
                           ask_int("id работы: "), ask_int("Оценка: "))
        print("Оценка выставлена")

    def change_price(self) -> None:
        course = self._p.courses.get(ask_int("id курса: "))
        course.price = ask_float("Новая цена: ")
        self._p.courses.update(course)
        print(f"Обновлено: {course}")

    # Delete
    def delete_course(self) -> None:
        self._p.delete_course(ask_int("id курса: "))
        print("Курс удалён")

    # Файлы
    @staticmethod
    def _ask_storage() -> Storage:
        choice = ask_text("Формат (1 - JSON, 2 - XML): ")
        if choice not in STORAGES:
            raise ValidationError("Нужно выбрать 1 или 2")
        storage_class, path = STORAGES[choice]
        return storage_class(path)

    def save(self) -> None:
        self._ask_storage().save(self._p)
        print("Сохранено")

    def load(self) -> None:
        self._p = self._ask_storage().load()
        print("Загружено")

    # Главный цикл
    def run(self) -> None:
        try:
            while True:
                print("\n=== Онлайн-обучение ===")
                for key, (title, _) in self._menu.items():
                    print(f"{key}. {title}")
                print("0. Выход")
                choice = input("Выберите пункт: ").strip()
                if choice == "0":
                    break
                if choice not in self._menu:
                    print("Нет такого пункта меню.")
                    continue
                try:
                    self._menu[choice][1]()
                except LearningError as error:
                    print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print()
        print("До свидания!")

# Запуск консоли
if __name__ == "__main__":
    ConsoleApp().run()
