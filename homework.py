import logging
import os
import requests
import time

from dotenv import load_dotenv
from telebot import TeleBot, types

from exceptions import TokenError

load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {practicum_token}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Ищет токены в переменных окружения."""
    if practicum_token and telegram_token and telegram_chat_id:
        return
    else:
        raise TokenError


def send_message(bot, message):
    ...


def get_api_answer(timestamp):
    payload = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    return response.json()


def check_response(response):
    ...


def parse_status(homework):
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    # Создаем объект класса бота
    bot = TeleBot(token=telegram_token)
    timestamp = int(time.time())

    check_tokens()

    while True:
        get_api_answer(timestamp)
        try:
            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
        ...

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
