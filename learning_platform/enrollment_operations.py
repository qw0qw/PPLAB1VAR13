from __future__ import annotations

from typing import TYPE_CHECKING

from models import Enrollment

if TYPE_CHECKING:
    from .core import LearningPlatform


class EnrollmentOperations:
    """Операции, связанные с записью студентов на курсы."""

    def enroll(self: LearningPlatform, student_id: int,
               course_id: int) -> Enrollment:
        """Записывает студента на курс."""
        student = self.students.get(student_id)
        course = self.courses.get(course_id)
        enrollment = Enrollment(
            self.next_id(self.enrollments), student, course
        )
        student.add_enrollment(enrollment)
        return self.enrollments.create(enrollment)
