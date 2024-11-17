class TokenError(Exception):
    """Исключение будет выброшено, если токены не будут найдены."""

    def __str__(self):
        """Исключение будет выброшено, если токены не будут найдены."""
        return 'Токены не были найдены'


class IncorrectTypeOfResponse(Exception):
    """Ответ API не удалось привести к типу данных Python."""

    def __str__(self):
        """Ответ API не удалось привести к типу данных Python."""
        return 'Ответ API не удалось привести к типу данных Python'
