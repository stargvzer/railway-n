import telebot
import kol
import threading
import requests
import random
import os

bot = telebot.TeleBot(kol.token)

# Путь к папке со стикерами
sticker_folder = 'stickers'  # Замените на реальный путь к вашей папке со стикерами

def keep_alive():
    # Периодический запрос к самому себе, чтобы контейнер не останавливался
    threading.Timer(300, keep_alive).start()  # Каждые 5 минут
    requests.get("https://railway-n-istoriya.up.railway.app")  # Замените на ваш Railway URL

keep_alive()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, kol.startAnswer)

# Обработчик сообщений с несколькими условиями
@bot.message_handler(func=lambda message: message.text and (
        '/meh' in message.text.lower() or
        'танк из озера, скажи свою мудрость' in message.text.lower() or
        'мать' in message.text.lower() or
        'шерст' in message.text.lower() or
        'мудрость от бабуина' in message.text.lower()  # Добавили новое условие
))
def handle_request(message):
    # Проверяем, какое ключевое слово/фраза была использована
    if 'мудрость от бабуина' in message.text.lower():
        prefix = "Шведский бабуин сказал: "  # Фраза для "мудрость от бабуина"
    else:
        prefix = "Мудрый танк из озера сказал: "  # Фраза по умолчанию

    random_message = kol.random_message()  # Получаем случайное сообщение
    bot.send_message(message.chat.id, f"{prefix}{random_message}")  # Отправляем сообщение с нужной фразой

# Обработчик команды для отправки случайного стикера по запросу (команда /mehp)
@bot.message_handler(commands=['mehp'])
def handle_random_sticker(message):
    chat_id = message.chat.id
    send_random_sticker(chat_id)

# Обработчик сообщений для отправки случайного стикера по текстовой команде "открытка от бабуина"
@bot.message_handler(func=lambda message: 'открытка от бабуина' in message.text.lower())
def handle_baboon_postcard(message):
    chat_id = message.chat.id
    send_random_sticker(chat_id)

# Функция для отправки случайного стикера
def send_random_sticker(chat_id):
    try:
        # Получаем список всех файлов в директории
        stickers = [f for f in os.listdir(sticker_folder) if os.path.isfile(os.path.join(sticker_folder, f))]

        if stickers:
            random_sticker = random.choice(stickers)  # Выбираем случайный стикер
            sticker_path = os.path.join(sticker_folder, random_sticker)

            # Отправляем стикер
            with open(sticker_path, 'rb') as sticker_file:
                bot.send_sticker(chat_id, sticker_file)
        else:
            bot.send_message(chat_id, "Не удалось найти стикеры в папке.")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при отправке стикера: {str(e)}")

# Функция для отправки случайного стикера в конференцию раз в час
def send_random_sticker_to_conference():
    chat_id = '-1001507836344'  # Замените на ID вашей конференции
    send_random_sticker(chat_id)

# Функция для планирования отправки случайных стикеров раз в час
def schedule_sticker_messages():
    send_random_sticker_to_conference()  # Отправляем стикер сразу
    threading.Timer(3600, schedule_sticker_messages).start()  # Повторяем через 1 час

# Функция для отправки случайного сообщения в чат
def send_random_message():
    chat_id = '-1001507836344'  # Замените на ID вашей группы
    random_message = kol.random_message()  # Получаем случайное сообщение

    # Добавляем фразу к сообщению
    message_to_send = f"Мудрый танк из озера сказал: {random_message}"
    bot.send_message(chat_id, message_to_send)  # Отправляем сообщение в чат

# Функция для планирования отправки сообщений раз в час
def schedule_messages():
    send_random_message()  # Отправляем сообщение сразу
    threading.Timer(3599, schedule_messages).start()  # Повторяем через 1 час

# Запуск бота и планирование сообщений
if __name__ == '__main__':
    schedule_sticker_messages()  # Запускаем планирование отправки стикеров раз в час
    schedule_messages()  # Запускаем планирование сообщений
    bot.polling(none_stop=True)