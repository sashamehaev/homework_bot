import logging
import os
import time

from http import HTTPStatus
from pprint import pprint
import requests
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import (
    HomeworkValuesError,
    NotContainHomeworkError,
    ServerResponseError,
    TokenError,
    SendMessageError,
    ResponseTypeDictError,
    ResponseHomeworksTypeListError,
    HomeworkStatusKeyError
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


logging.basicConfig(
    format=LOGGING_FORMAT,
    level=logging.DEBUG
)


def check_tokens():
    """Ищет токены в переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return
    else:
        logging_tokens = dict(
            PRACTICUM_TOKEN=PRACTICUM_TOKEN,
            TELEGRAM_TOKEN=TELEGRAM_TOKEN,
            TELEGRAM_CHAT_ID=TELEGRAM_CHAT_ID
        )
        print(logging_tokens)
        logging.critical(
            f'{logging_tokens} Не все обязательные токены заполнены.'
        )
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
        payload = {'from_date': timestamp}
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception:
        logging.debug('Не удалось получить ответ API.')
    if response.status_code != HTTPStatus.OK:
        raise ServerResponseError
    return response.json()


def check_response(response):
    """Проверяет ответ на соответствие типам и значениям."""
    if not isinstance(response['homeworks'], list):
        raise ResponseHomeworksTypeListError
    if 'homeworks' not in response:
        raise KeyError
    if not isinstance(response, dict):
        raise ResponseTypeDictError


def parse_status(homework):
    """Подготавливает ответ API."""
    if homework['status'] not in HOMEWORK_VERDICTS:
        raise HomeworkValuesError
    if 'status' not in homework:
        raise HomeworkStatusKeyError
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
    main()
