import telebot
import kol
import threading

bot = telebot.TeleBot(kol.token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, kol.startAnswer)

# Обработчик сообщений, содержащих команду или ключевое слово
@bot.message_handler(func=lambda message: message.text and (
    '/meh' in message.text.lower() or 'танк из озера, скажи свою мудрость' in message.text.lower()
))
def handle_request(message):
    random_message = kol.random_message()  # Получаем случайное сообщение
    bot.send_message(message.chat.id, random_message)

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
    threading.Timer(3600, schedule_messages).start()  # Повторяем через 1 час

# Запуск бота и планирование сообщений
if __name__ == '__main__':
    schedule_messages()  # Запускаем планирование
    bot.polling(none_stop=True)