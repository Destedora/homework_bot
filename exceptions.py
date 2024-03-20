class EnvVarError(Exception):
    """Исключение отсутствия переменных окружения."""

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Отсутсвуют переменные окружения'

    def __str__(self):
        return self.message


class SendException(Exception):
    """Ошибка, возникающая при неудачной отправке сообщения."""
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Ошибка отправки сообщения :('

    def __str__(self):
        return self.message


class StatusCodeError(Exception):
    """Ошибка статуса ответа."""

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Status_code != 200'

    def __str__(self):
        return self.message


class EmptyAPIAnswerError(Exception):
    """Ошибка отсутствия ключа."""

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Неверное значение параметра "homeworks"'

    def __str__(self):
        return self.message


class RequestError(Exception):
    """Ошибка запроса."""

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Ошибка запроса к API'

    def __str__(self):
        return self.message
