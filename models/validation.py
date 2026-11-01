from exceptions.validation_error import ValidationError


def require_text(value: str, field: str) -> str:
    """Проверяет, что значение является непустой строкой."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Поле '{field}' не может быть пустым")
    return value.strip()
