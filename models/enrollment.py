from exceptions.validation_error import ValidationError


class Enrollment:
    """Запись студента на курс с прогрессом."""

    def __init__(self, enrollment_id: int, student: "Student",
                 course: "Course") -> None:
        self.id = enrollment_id
        self.student = student
        self.course = course
        self.progress = 0.0

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
