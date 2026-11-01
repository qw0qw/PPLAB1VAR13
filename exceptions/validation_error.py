from exceptions.learning_error import LearningError



class ValidationError(LearningError):
    """Некорректное значение (пустая строка, отрицательная цена, оценка)."""