import logging
import sys
import time
from http import HTTPStatus

import requests
import telegram


from exceptions import (
    EmptyAPIAnswerError,
    StatusCodeError,
    EnvVarError,
    RequestError,
    SendException
)
from settings import (
    PRACTICUM_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN,
    RETRY_PERIOD,
    ENDPOINT,
    HOMEWORK_VERDICTS,
    HEADERS
)

logger = logging.getLogger(__name__)


def check_tokens():
    """Проверка доступности переменных окружения."""
    if not all([TELEGRAM_TOKEN, PRACTICUM_TOKEN, TELEGRAM_CHAT_ID]):
        logger.critical('Отсутствуют обязательные переменные окружения')
        raise EnvVarError


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logger.debug('Начинаем отправлять сообщение...')
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
    except telegram.error.TelegramError as error:
        logger.error(f'Не удалось отправить сообщение: {error}')
        raise SendException
    logger.debug(f'Сообщение успешно отправлено: {message}')


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    logger.debug('Получаем новые статусы...')
    try:
        response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp},
        )
        if response.status_code != HTTPStatus.OK:
            raise StatusCodeError
        return response.json()
    except requests.exceptions.RequestException:
        raise RequestError


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    logger.debug('Проверяем ответ сервара')
    if not isinstance(response, dict):
        raise TypeError(
            f'Тип {type(response)} не соответствует'
            f' ожидаемому {type(dict())}'
        )
    homeworks = response.get('homeworks')
    if homeworks is None:
        raise EmptyAPIAnswerError
    if not isinstance(homeworks, list):
        raise TypeError(
            f'Тип {type(response)} не соответствует'
            f' ожидаемому {type(list())})'
        )
    return homeworks


def parse_status(homework):
    """Извлекает из домашней работы её статус."""
    logging.info('Начало парсинга')
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError('Не найден ключ "homework_name"')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус работы: {homework_status}')
    verdict = HOMEWORK_VERDICTS.get(homework_status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    logger.debug('Запуск')
    check_tokens()
    logger.debug('Переменные окружения проверены')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    old_status = None
    while True:
        try:
            answer = get_api_answer(timestamp)
            timestamp = answer.get('current_date', timestamp)
            homeworks = check_response(answer)
            if homeworks:
                new_status = parse_status(homeworks[0])
            else:
                new_status = 'Новый статус пока отсутствует'
                logger.debug(new_status)
            if old_status != new_status:
                send_message(bot, new_status)
                old_status = new_status
        except (StatusCodeError, EmptyAPIAnswerError,
                RequestError, TypeError,
                KeyError, ValueError) as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if message != old_status:
                send_message(bot, message)
                old_status = message
        except Exception as error:
            message = f'Непредвиденная ошибка: {error}'
            logger.error(message)
            if message != old_status:
                send_message(bot, message)
                old_status = message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(lineno)d - '
        '%(funcName)s - %(levelname)s - %(message)s'
    )
    stream_handler = logging.StreamHandler(
        stream=sys.stdout
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(
        filename=__file__ + '.log', encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    main()
