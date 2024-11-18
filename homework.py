import logging
import os
import requests
import time

from pprint import pprint
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import (
    TokenError,
    ServerResponseError,
    NotContainHomeworkError,
    HomeworkValuesError
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format='%(lineno)d – %(levelname)s: %(message)s',
    level=logging.DEBUG
)


def check_tokens():
    """Ищет токены в переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return
    else:
        raise TokenError


def send_message(bot, message):
    """Отправляет результат пользователю в телеграмм."""


def get_api_answer(timestamp):
    """Получает ответ от API и приводит его к типу данных Python."""
    try:
        payload = {'from_date': timestamp}
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except requests.RequestException as error:
        message = f'Сбой в работе программы: {error}'
        print(message)
    if response.status_code != 200:
        raise ServerResponseError
    return response.json()


def check_response(response):
    """..."""
    if 'homeworks' not in response:
        raise TypeError
    if not isinstance(response, dict):
        raise TypeError
    if not isinstance(response['homeworks'], list):
        raise TypeError


def parse_status(homework):
    """Подготавливает ответ API."""
    if homework['status'] not in HOMEWORK_VERDICTS or 'status' not in homework:
        raise HomeworkValuesError
    if 'homework_name' not in homework:
        raise NotContainHomeworkError
    homework_name = homework['homework_name']
    verdict = HOMEWORK_VERDICTS[homework['status']]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    # Создаем объект класса бота
    check_tokens()
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            parse_status(response['homeworks'][0])
        except Exception as error:
            logging.error(error)
            message = f'Сбой в работе программы: {error}'
            print(message)

        time.sleep(600)


if __name__ == '__main__':
    main()
