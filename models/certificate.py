from exceptions.validation_error import ValidationError


class Certificate:
    """Сертификат о завершении курса."""

    def __init__(self, certificate_id: int, enrollment: "Enrollment") -> None:
        if not enrollment.is_completed():
            raise ValidationError("Курс ещё не пройден до конца")
        self.id = certificate_id
        self.enrollment = enrollment

    def __str__(self) -> str:
        return (f"Сертификат #{self.id}: {self.enrollment.student.name} "
                f"успешно завершил(а) курс «{self.enrollment.course.title}»")
