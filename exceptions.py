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
    """В ответе API нет ключа 'homework_name'."""

    def __str__(self):
        """В ответе API нет ключа 'homework_name'."""
        return 'В ответе API нет ключа "homework_name".'


class HomeworkValuesError(Exception):
    """API прислало задание с неверным статусом."""

    def __str__(self):
        """API прислало задание с неверным статусом."""
        return 'API прислало задание с неверным статусом.'


class SendMessageError(Exception):
    """API не удалось отправить сообщение пользователю."""

    def __str__(self):
        """API не удалось отправить сообщение пользователю."""
        return 'API не удалось отправить сообщение пользователю.'


class KeyError(Exception):
    """Не удалось найти ключ homeworks в ответе API."""

    def __str__(self):
        """Не удалось найти ключ homeworks в ответе API."""
        return 'Не удалось найти ключ homeworks в ответе API.'


class ResponseDictTypeError(TypeError):
    """Неверный тип. Ожидаемый тип dict."""

    def __str__(self):
        """Неверный тип. Ожидаемый тип dict."""
        return 'Неверный тип. Ожидаемый тип dict.'


class ResponseHomeworksListTypeError(TypeError):
    """Неверный тип данных списка домашних работ. Ожидаемый тип list."""

    def __str__(self):
        """Неверный тип данных списка домашних работ. Ожидаемый тип list."""
        return 'Неверный тип данных списка домашних работ. Ожидаемый тип list.'


class HomeworkStatusKeyError(Exception):
    """Остутсвует ключ 'status' в ответе API."""

    def __str__(self):
        """Остутсвует ключ 'status' в ответе API."""
        return 'Остутсвует ключ "status" в ответе API.'
