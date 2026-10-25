class LearningError(Exception):
    """Базовое исключение всех ошибок приложения."""


class ValidationError(LearningError):
    """Некорректное значение (пустая строка, отрицательная цена, оценка)."""


class EntityNotFoundError(LearningError):
    """Объект с указанным id не найден."""


class DuplicateEntityError(LearningError):
    """Объект с таким id или такая запись уже существует."""


class StorageError(LearningError):
    """Ошибка чтения или записи файла (JSON, XML)."""