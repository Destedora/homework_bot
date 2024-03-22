class MinorError(Exception):
    """Базовый класс для несущественных ошибок."""
    MESSAGE = None

    def __init__(self):
        message = self.MESSAGE
        super().__init__(message)


class EnvVarError(MinorError):
    """Исключение отсутствия переменных окружения."""
    MESSAGE = 'Отсутсвуют переменные окружения'


class SendException(MinorError):
    """Ошибка, возникающая при неудачной отправке сообщения."""
    MESSAGE = 'Ошибка отправки сообщения :('


class StatusCodeError(MinorError):
    """Ошибка статуса ответа."""
    MESSAGE = 'Status_code != 200'


class EmptyAPIAnswerError(MinorError):
    """Ошибка отсутствия ключа."""
    MESSAGE = 'Неверное значение параметра "homeworks"'


class RequestError(MinorError):
    """Ошибка запроса."""
    MESSAGE = 'Ошибка запроса к API'
