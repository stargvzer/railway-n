import telebot
import random
import threading
import os

# Ваш Telegram-токен
TELEGRAM_TOKEN = '5257043486:AAFgddkVAq9Ls0EwjMLi8PFlGjj_uKI3zrw'  # Замените на ваш токен

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Путь к текстовому файлу с сообщениями
current_dir = os.path.dirname(os.path.abspath(__file__))
text_file = os.path.join(current_dir, 'clean_text.txt')  # Замените на имя вашего текстового файла

# Функция для чтения текстового файла и извлечения сообщений
def get_messages_from_text():
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            messages = file.readlines()  # Читаем все строки в файл
            # Удаляем пробелы и пустые строки
            messages = [msg.strip() for msg in messages if msg.strip()]
            return messages
    except FileNotFoundError:
        return []

# Функция для выбора случайного сообщения
def get_random_message():
    messages = get_messages_from_text()
    if messages:
        return random.choice(messages)
    return "Не удалось найти сообщения в файле."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    random_message = get_random_message()  # Получаем случайное сообщение
    bot.send_message(message.chat.id, random_message)

# Обработчик сообщений, содержащих команду /meh или ключевое слово
@bot.message_handler(func=lambda message: message.text and (
        '/meh' in message.text or
        'шерстушение' in message.text.lower()
    ))
def handle_request(message):
    random_message = get_random_message()  # Получаем случайное сообщение
    bot.send_message(message.chat.id, random_message)

# Функция для отправки случайного сообщения в чат
def send_random_message():
    chat_id = '-1001507836344'  # Замените на ID вашей группы
    random_message = get_random_message()  # Получаем случайное сообщение

    # Добавляем фразу к сообщению
    message_to_send = f"Мудрый танк из озера сказал: {random_message}"
    bot.send_message(chat_id, message_to_send)  # Отправляем сообщение в чат

# Функция для планирования отправки сообщений раз в час
def schedule_messages():
    send_random_message()  # Отправляем сообщение сразу
    threading.Timer(3600, schedule_messages).start()  # Повторяем через 1 час

# Запуск бота и планирование сообщений
if __name__ == '__main__':
    schedule_messages()  # Запускаем планирование
    bot.polling(none_stop=True)