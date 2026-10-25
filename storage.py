"""Сохранение и загрузка данных в форматах JSON и XML."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any

from exceptions import LearningError, StorageError
from learning_platform import LearningPlatform
from models import (
    Assignment,
    Category,
    Certificate,
    Course,
    Enrollment,
    Lesson,
    Module,
    Student,
    Submission,
    Teacher,
)


# Объекты <---> словарь
def platform_to_dict(p: LearningPlatform) -> dict[str, Any]:
    """Превращает все данные платформы в словарь."""
    return {
        "teachers": [
            {"id": t.id, "name": t.name, "email": t.email,
             "department": t.department} for t in p.teachers.get_all()],
        "students": [
            {"id": s.id, "name": s.name, "email": s.email,
             "group": s.group} for s in p.students.get_all()],
        "categories": [
            {"id": c.id, "name": c.name} for c in p.categories.get_all()],
        "courses": [
            {"id": c.id, "title": c.title, "price": c.price,
             "teacher_id": c.teacher.id, "category_id": c.category.id,
             "modules": [
                 {"id": m.id, "title": m.title,
                  "lessons": [
                      {"id": ls.id, "title": ls.title,
                       "duration_min": ls.duration_min}
                      for ls in m.lessons]}
                 for m in c.modules]}
            for c in p.courses.get_all()],
        "assignments": [
            {"id": a.id, "title": a.title, "max_score": a.max_score}
            for a in p.assignments.get_all()],
        "enrollments": [
            {"id": e.id, "student_id": e.student.id,
             "course_id": e.course.id, "progress": e.progress}
            for e in p.enrollments.get_all()],
        "submissions": [
            {"id": s.id, "student_id": s.student.id,
             "assignment_id": s.assignment.id, "text": s.text,
             "score": s.score} for s in p.submissions.get_all()],
        "certificates": [
            {"id": c.id, "enrollment_id": c.enrollment.id}
            for c in p.certificates.get_all()],
    }


def platform_from_dict(data: dict[str, Any]) -> LearningPlatform:
    """Собирает платформу из словаря."""
    p = LearningPlatform()
    for d in data["teachers"]:
        p.teachers.create(
            Teacher(d["id"], d["name"], d["email"], d["department"]))
    for d in data["students"]:
        p.students.create(
            Student(d["id"], d["name"], d["email"], d["group"]))
    for d in data["categories"]:
        p.categories.create(Category(d["id"], d["name"]))
    for d in data["courses"]:
        course = Course(d["id"], d["title"], d["price"],
                        p.teachers.get(d["teacher_id"]),
                        p.categories.get(d["category_id"]))
        for m in d["modules"]:
            module = Module(m["id"], m["title"])
            for ls in m["lessons"]:
                module.add_lesson(
                    Lesson(ls["id"], ls["title"], ls["duration_min"]))
            course.add_module(module)
        p.courses.create(course)
        course.teacher.courses.append(course)
        course.category.courses.append(course)
    for d in data["assignments"]:
        p.assignments.create(
            Assignment(d["id"], d["title"], d["max_score"]))
    for d in data["enrollments"]:
        student = p.students.get(d["student_id"])
        enrollment = p.enrollments.create(
            Enrollment(d["id"], student, p.courses.get(d["course_id"])))
        enrollment.progress = d["progress"]
        student.add_enrollment(enrollment)
    for d in data["submissions"]:
        submission = p.submissions.create(Submission(
            d["id"], p.students.get(d["student_id"]),
            p.assignments.get(d["assignment_id"]), d["text"]))
        if d["score"] is not None:
            submission.score = d["score"]
    for d in data["certificates"]:
        p.certificates.create(
            Certificate(d["id"], p.enrollments.get(d["enrollment_id"])))
    return p

def _restore(data: Any) -> LearningPlatform:
    """Собирает платформу; любой сбой структуры - это StorageError."""
    try:
        return platform_from_dict(data)
    except (KeyError, TypeError, ValueError, LearningError) as error:
        raise StorageError(f"Некорректные данные в файле: {error!r}") \
            from error


# Хранилища
class Storage(ABC):
    """Абстрактное файловое хранилище."""

    def __init__(self, path: str) -> None:
        self._path = path

    @abstractmethod
    def save(self, platform: LearningPlatform) -> None:
        """Записывает данные платформы в файл."""

    @abstractmethod
    def load(self) -> LearningPlatform:
        """Читает файл и возвращает платформу."""


class JsonStorage(Storage):
    """Хранилище в формате JSON."""

    def save(self, platform: LearningPlatform) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                json.dump(platform_to_dict(platform), file,
                          ensure_ascii=False, indent=2)
        except OSError as error:
            raise StorageError(f"Не удалось записать файл: {error}") \
                from error

    def load(self) -> LearningPlatform:
        try:
            with open(self._path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise StorageError(f"Файл {self._path} не найден") from None
        except (OSError, ValueError) as error:   # JSONDecodeError - ValueError
            raise StorageError(f"Не удалось прочитать файл: {error}") \
                from error
        return _restore(data)


# JSON готов, дальше идёт XML хранилищею
def _to_xml(parent: ET.Element, tag: str, value: Any) -> None:
    """Рекурсивно записывает значение в XML (тип хранится в атрибуте)."""
    element = ET.SubElement(parent, tag)
    if isinstance(value, dict):
        for key, item in value.items():
            _to_xml(element, key, item)
    elif isinstance(value, list):
        element.set("type", "list")
        for item in value:
            _to_xml(element, "item", item)
    elif value is None:
        element.set("type", "none")
    else:
        element.set("type", type(value).__name__)
        element.text = str(value)


def _from_xml(element: ET.Element) -> Any:
    """Обратное преобразование XML-элемента в значение Python."""
    kind = element.get("type")
    if kind == "list":
        return [_from_xml(child) for child in element]
    if kind == "none":
        return None
    if kind is None:    # элемент без типа - словарь
        return {child.tag: _from_xml(child) for child in element}
    converters = {"int": int, "float": float, "str": str}
    return converters[kind](element.text or "")


class XmlStorage(Storage):
    """Хранилище в формате XML."""

    def save(self, platform: LearningPlatform) -> None:
        root = ET.Element("platform")
        for key, value in platform_to_dict(platform).items():
            _to_xml(root, key, value)
        tree = ET.ElementTree(root)
        ET.indent(tree)
        try:
            tree.write(self._path, encoding="utf-8", xml_declaration=True)
        except OSError as error:
            raise StorageError(f"Не удалось записать файл: {error}") \
                from error

    def load(self) -> LearningPlatform:
        try:
            root = ET.parse(self._path).getroot()
        except FileNotFoundError:
            raise StorageError(f"Файл {self._path} не найден") from None
        except (OSError, ET.ParseError) as error:
            raise StorageError(f"Не удалось прочитать файл: {error}") \
                from error
        try:
            data = {child.tag: _from_xml(child) for child in root}
        except (KeyError, ValueError) as error:
            raise StorageError(f"Неверный формат XML: {error!r}") from error
        return _restore(data)