import telebot
import random
from bs4 import BeautifulSoup
import threading
import os

# Ваш Telegram-токен вместо kol.token
TELEGRAM_TOKEN = '5257043486:AAFgddkVAq9Ls0EwjMLi8PFlGjj_uKI3zrw'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Путь к HTML-файлу с историей чата
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(current_dir, 'history.html')


# Функция для чтения HTML-файла и извлечения сообщений
def get_messages_from_html():
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Находим все элементы с классом 'text', которые содержат сообщения
            messages = [div.get_text(strip=True) for div in soup.find_all('div', class_='text')]
            return messages
    except FileNotFoundError:
        return []


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    messages = get_messages_from_html()
    if messages:
        random_message = random.choice(messages)  # Выбираем случайное сообщение
        bot.send_message(message.chat.id, random_message)
    else:
        bot.send_message(message.chat.id, "История сообщений не найдена.")


# Обработчик сообщений, содержащих команду /request или ключевое слово
@bot.message_handler(
    func=lambda message: message.text and (
        '/meh' in message.text or
        'Танк из озера, скажи свою мудрость' in message.text.lower()
    )
)
def handle_request(message):
    messages = get_messages_from_html()
    if messages:
        random_message = random.choice(messages)  # Выбираем случайное сообщение
        bot.send_message(message.chat.id, random_message)
    else:
        bot.send_message(message.chat.id, "Не удалось найти сообщения в файле.")


# Функция для выбора случайного сообщения и отправки его в чат
def send_random_message():
    chat_id = '-1001507836344'  # Замените на ID вашей группы
    messages = get_messages_from_html()

    if messages:
        random_message = random.choice(messages)  # Выбираем случайное сообщение
        bot.send_message(chat_id, random_message)  # Отправляем сообщение в чат
    else:
        bot.send_message(chat_id, "Не удалось найти сообщения в файле.")


# Функция для планирования отправки сообщений раз в час
def schedule_messages():
    send_random_message()  # Отправляем сообщение сразу
    threading.Timer(3600, schedule_messages).start()  # Повторяем через 1 час


# Запуск бота и планирование сообщений
if __name__ == '__main__':
    schedule_messages()  # Запускаем планирование
    bot.polling(none_stop=True)
