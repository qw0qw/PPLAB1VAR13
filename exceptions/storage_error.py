from exceptions.learning_error import LearningError



class StorageError(LearningError):
    """Ошибка чтения или записи файла (JSON, XML)."""