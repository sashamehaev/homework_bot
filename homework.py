import logging
import os
import requests
import time
from pprint import pprint

from dotenv import load_dotenv
from telebot import TeleBot, types

from exceptions import TokenError, IncorrectTypeOfResponse

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
    """Получает ответ от API и приводит его к типу данных Python."""
    payload = {'from_date': 0}
    response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    return response.json()


def check_response(response):
    """Проверяет тип данных ответа API."""
    if not isinstance(response, dict):
        raise IncorrectTypeOfResponse


def parse_status(homework):
    homework_name = homework['homework_name']
    verdict = homework['status']
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    # Создаем объект класса бота
    bot = TeleBot(token=telegram_token)
    timestamp = int(time.time())

    check_tokens()

    while True:
        response = get_api_answer(timestamp)
        check_response(response)
        homework = response['homeworks'][0]
        print(parse_status(homework))
        try:
            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'

        bot.polling()

if __name__ == '__main__':
    main()
