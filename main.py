import telebot
import kol
import schedule
import time
from threading import Thread

bot = telebot.TeleBot(kol.token)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, kol.startAnswer)


# Обработчик сообщений, содержащих команду /request или ключевое слово
@bot.message_handler(
    func=lambda message: message.text and ('/meh' in message.text or 'шерсть' in message.text.lower()))
def handle_request(message):
    bot.send_message(message.chat.id, kol.random_message())


# Функция для отправки случайного сообщения в конференцию
def send_random_message():
    # Здесь нужно указать chat_id вашей конференции
    chat_id = "-1001507836344"
    bot.send_message(chat_id, kol.random_message())


# Планирование задачи каждые 4 часа
def schedule_message_posting():
    schedule.every(30).minutes.do(send_random_message)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем задачи каждую минуту


# Запускаем планирование в отдельном потоке, чтобы бот мог параллельно работать
def start_scheduler():
    scheduler_thread = Thread(target=schedule_message_posting)
    scheduler_thread.start()


if __name__ == '__main__':
    start_scheduler()  # Запускаем планировщик
    bot.polling(none_stop=True)  # Запускаем бота
