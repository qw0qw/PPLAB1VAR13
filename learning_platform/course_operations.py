from __future__ import annotations

from typing import TYPE_CHECKING

from exceptions.validation_error import ValidationError

if TYPE_CHECKING:
    from .core import LearningPlatform


class CourseOperations:
    """Операции управления курсами."""

    def delete_course(self: LearningPlatform, course_id: int) -> None:
        """Удаляет курс, если на него никто не записан."""
        course = self.courses.get(course_id)

        if any(
            enrollment.course.id == course_id
            for enrollment in self.enrollments.get_all()
        ):
            raise ValidationError(
                "Нельзя удалить курс: на него есть записи"
            )

        course.teacher.courses.remove(course)
        course.category.courses.remove(course)
        self.courses.delete(course_id)
