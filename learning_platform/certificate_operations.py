from __future__ import annotations

from typing import TYPE_CHECKING

from models import Certificate
from exceptions.duplicate_entity_error import DuplicateEntityError

if TYPE_CHECKING:
    from .core import LearningPlatform


class CertificateOperations:
    """Операции по выдаче сертификатов."""

    def issue_certificate(self: LearningPlatform,
                          enrollment_id: int) -> Certificate:
        """Выдаёт сертификат за завершённый курс."""
        enrollment = self.enrollments.get(enrollment_id)

        for certificate in self.certificates.get_all():
            if certificate.enrollment.id == enrollment_id:
                raise DuplicateEntityError("Сертификат уже выдан")

        return self.certificates.create(
            Certificate(self.next_id(self.certificates), enrollment)
        )
