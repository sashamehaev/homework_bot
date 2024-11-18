class TokenError(Exception):
    """Исключение будет выброшено, если токены не будут найдены."""

    def __str__(self):
        """Исключение будет выброшено, если токены не будут найдены."""
        return 'Токены не были найдены'


class ResponseTypeError(Exception):
    """Ответ API не удалось привести к типу данных Python."""

    def __str__(self):
        """Ответ API не удалось привести к типу данных Python."""
        return 'Ответ API не удалось привести к типу данных Python.'


class HomeworkIndexError(Exception):
    """От API не было получено ни одной записи."""

    def __str__(self):
        """От API не было получено ни одной записи."""
        return 'От API не было получено ни одной записи.'


class ServerResponseError(Exception):
    """Не удалось получить успешный ответ от API."""

    def __str__(self):
        """Не удалось получить успешный ответ от API."""
        return 'Не удалось получить успешный ответ от API.'


class NotContainHomeworkError(Exception):
    """В ответе API не попали домашние работы."""

    def __str__(self):
        """В ответе API не попали домашние работы."""
        return 'В ответе API не попали домашние работы.'


class HomeworkValuesError(Exception):
    """API прислало задание с неверным статусом."""

    def __str__(self):
        """API прислало задание с неверным статусом."""
        return 'API прислало задание с неверным статусом.'
