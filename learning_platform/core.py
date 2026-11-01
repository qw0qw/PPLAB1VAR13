from __future__ import annotations

from models import (
    Assignment,
    Category,
    Certificate,
    Course,
    Enrollment,
    Student,
    Submission,
    Teacher,
)
from repository import Repository

from .assignment_operations import AssignmentOperations
from .certificate_operations import CertificateOperations
from .course_operations import CourseOperations
from .enrollment_operations import EnrollmentOperations


class LearningPlatform(
    EnrollmentOperations,
    CertificateOperations,
    AssignmentOperations,
    CourseOperations,
):
    """Основной класс платформы, объединяющий репозитории и операции."""

    def __init__(self) -> None:
        self.teachers: Repository[Teacher] = Repository("Преподаватель")
        self.students: Repository[Student] = Repository("Студент")
        self.categories: Repository[Category] = Repository("Категория")
        self.courses: Repository[Course] = Repository("Курс")
        self.enrollments: Repository[Enrollment] = Repository("Запись")
        self.assignments: Repository[Assignment] = Repository("Задание")
        self.submissions: Repository[Submission] = Repository("Работа")
        self.certificates: Repository[Certificate] = Repository("Сертификат")

    @staticmethod
    def next_id(repo: Repository) -> int:
        """Возвращает следующий свободный id в репозитории."""
        return max(
            (item.id for item in repo.get_all()),
            default=0,
        ) + 1
