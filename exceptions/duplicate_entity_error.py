from exceptions.learning_error import LearningError



class DuplicateEntityError(LearningError):
    """Объект с таким id или такая запись уже существует."""