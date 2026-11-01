from __future__ import annotations

from typing import TYPE_CHECKING

from models import Submission

if TYPE_CHECKING:
    from .core import LearningPlatform


class AssignmentOperations:
    """Операции по сдаче и проверке заданий."""

    def submit_work(self: LearningPlatform, student_id: int,
                    assignment_id: int, text: str) -> Submission:
        """Студент сдаёт работу по заданию."""
        return self.submissions.create(
            Submission(
                self.next_id(self.submissions),
                self.students.get(student_id),
                self.assignments.get(assignment_id),
                text,
            )
        )

    def grade_work(self: LearningPlatform, teacher_id: int,
                   submission_id: int, score: int) -> None:
        """Преподаватель оценивает работу."""
        teacher = self.teachers.get(teacher_id)
        submission = self.submissions.get(submission_id)
        teacher.grade(submission, score)
