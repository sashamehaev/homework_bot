import logging
import os
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telebot import TeleBot
from pprint import pprint

from exceptions import (
    HomeworkStatusError,
    NotContainHomeworkError,
    ServerResponseError,
    TokenError
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
LOGGING_FORMAT = '%(asctime)s, %(lineno)d, %(levelname)s: %(message)s'
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Ищет токены в переменных окружения."""
    logging_tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
    }
    for token in logging_tokens:
        if not logging_tokens[token]:
            logging.critical(f'Отсутствует токен {token}.')
            raise TokenError


def send_message(bot, message):
    """Отправляет результат пользователю в телеграмм."""
    logging.debug('Сообщение отправляется пользователю.')
    try:
        result = bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug(f'Сообщение {result.text} отправлено пользователю.')
    except Exception:
        logging.error('Сбой при отправке сообщения в телеграмм.')


def get_api_answer(timestamp):
    """Получает ответ от API и приводит его к типу данных Python."""
    logging.debug('Ожидание ответа API.')
    try:
        payload = {'from_date': 0}
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception:
        logging.debug('Не удалось получить ответ API.')
    if response.status_code != HTTPStatus.OK:
        raise ServerResponseError
    return response.json()


def check_response(response):
    """Проверяет ответ на соответствие типам и значениям."""
    if not isinstance(response, dict):
        raise TypeError(
            'В ответе API неверный тип данных. Ожидаемый тип dict.'
        )
    if 'homeworks' not in response:
        raise KeyError('Не удалось найти ключ homeworks в ответе API.')
    if not isinstance(response['homeworks'], list):
        raise TypeError(
            """В ответе API неверный тип данных домашних работ.
            Ожидаемый тип list."""
        )


def parse_status(homework):
    """Подготавливает ответ API."""
    if homework['status'] not in HOMEWORK_VERDICTS:
        raise ValueError(
            """В словаре HOMEWORK_VERDICTS
            нет значения из домашней работы под ключем "status" ответа API."""
        )
    if 'homework_name' not in homework:
        raise KeyError('В домашней работе нет ключа homework_name')
    if 'status' not in homework:
        raise KeyError('В домашней работе нет ключа "status"')
    homework_name = homework['homework_name']
    verdict = HOMEWORK_VERDICTS[homework['status']]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    # Создаем объект класса бота
    check_tokens()
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_status = ''
    while True:
        try:
            response = get_api_answer(timestamp)
            if not response['homeworks']:
                logging.debug('Статус домашнего задания не изменился.')
            check_response(response)
            message = parse_status(response['homeworks'][0])
            if last_status != message:
                send_message(bot, message)
            last_status = message
        except Exception as error:
            logging.error(error)
            message = f'Сбой в работе программы: {error}'
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format=LOGGING_FORMAT,
        level=logging.DEBUG
    )
    main()
