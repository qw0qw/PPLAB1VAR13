"""Хранилища и операции над несколькими классами сразу."""
from __future__ import annotations

from exceptions import DuplicateEntityError, ValidationError
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


class LearningPlatform:
    """Платформа онлайн-обучения."""

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
        """Следующий свободный id для репозитория."""
        return max((item.id for item in repo.get_all()), default=0) + 1

    def enroll(self, student_id: int, course_id: int) -> Enrollment:
        """Записывает студента на курс."""
        student = self.students.get(student_id)
        course = self.courses.get(course_id)
        enrollment = Enrollment(self.next_id(self.enrollments),
                                student, course)
        student.add_enrollment(enrollment)    # проверка на повторную запись
        return self.enrollments.create(enrollment)

    def issue_certificate(self, enrollment_id: int) -> Certificate:
        """Выдаёт сертификат за завершённый курс."""
        enrollment = self.enrollments.get(enrollment_id)
        for cert in self.certificates.get_all():
            if cert.enrollment.id == enrollment_id:
                raise DuplicateEntityError("Сертификат уже выдан")
        return self.certificates.create(
            Certificate(self.next_id(self.certificates), enrollment))

    def submit_work(self, student_id: int, assignment_id: int,
                    text: str) -> Submission:
        """Студент сдаёт работу по заданию."""
        return self.submissions.create(Submission(
            self.next_id(self.submissions),
            self.students.get(student_id),
            self.assignments.get(assignment_id), text))

    def grade_work(self, teacher_id: int, submission_id: int,
                   score: int) -> None:
        """Преподаватель оценивает работу."""
        self.teachers.get(teacher_id).grade(
            self.submissions.get(submission_id), score)

    def delete_course(self, course_id: int) -> None:
        """Удаляет курс, если на него никто не записан."""
        course = self.courses.get(course_id)
        if any(e.course.id == course_id for e in self.enrollments.get_all()):
            raise ValidationError("Нельзя удалить курс: на него есть записи")
        course.teacher.courses.remove(course)
        course.category.courses.remove(course)
        self.courses.delete(course_id)