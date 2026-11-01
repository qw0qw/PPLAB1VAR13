"""Модели предметной области платформы онлайн-обучения."""

from .validation import require_text
from .user import User
from .student import Student
from .teacher import Teacher
from .category import Category
from .lesson import Lesson
from .module import Module
from .course import Course
from .enrollment import Enrollment
from .assignment import Assignment
from .submission import Submission
from .certificate import Certificate

__all__ = [
    "require_text", "User", "Student", "Teacher", "Category", "Lesson",
    "Module", "Course", "Enrollment", "Assignment", "Submission",
    "Certificate",
]
