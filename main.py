from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
from datetime import datetime
import os

# Загрузка переменных окружения
load_dotenv(".env")
TG_TOKEN = os.getenv("TG_TOKEN")

# Сохраняем инициализированный объект бота
bot = TeleBot(TG_TOKEN)

# Хранилище данных пользователей
tasks: list[list[str]] = []


@bot.message_handler(commands=['start', 'help'])
def start_message(message: Message) -> None:
    """Отправляет приветственное сообщение и помощь по использованию бота."""
    welcome_text = """
    Привет! Я бот для управления задачами. Вот как со мной работать:
    - чтобы отправить задачу, отправьте в одном сообщении /add_task Название Описание
    - чтобы посмотреть все ваши задачи, отправьте /show_tasks
    - чтобы удалить задачу отправьте /del_task и введите номер задачи
    - чтобы посмотреть эту памятку снова, отправьте /help
    """

    user_id: int = message.chat.id
    bot.send_message(user_id, welcome_text)


@bot.message_handler(commands=['add_task'])
def add_task(message: Message) -> None:
    """Обрабатывает команду / add_task"""
    user_id: int = message.chat.id
    text: str = message.text[9:].strip()  # Берем слайс после '/add_task'

    if not text:
        bot.send_message(user_id, "Вы не указали задачу. Памятка - /help")
        return
    else:
        current_time = datetime.now().strftime('%d-%m-Y %H:%M')
        task_with_time = f"{current_time}- {text}"  # Добавляем время создания задачи
        bot.send_message(user_id, 'Ваша задача записана, для просмотра введите /show_tasks')

        task_parts = task_with_time.split('.')  # Для разделения задач
        tasks.append(task_parts)  # Для сохранения задач


@bot.message_handler(commands=['del_task'])
def delete_task(message: Message) -> None:
    """Обрабатывает команду /del_task"""
    user_id: int = message.chat.id
    text: str = message.text[10:].strip()  # берём текст после '/del_task'

    if not text.isdigit():
        bot.send_message(user_id, "Пожалуйста, введите номер задачи для удаления.")
        return

    task_index = int(text)
    if 1 <= task_index <= len(tasks):
        tasks.pop(task_index - 1)  # удаляем задачу с указанным номером
        bot.send_message(user_id, "Ваша задача удалена. Для просмотра списка ваших задач введите /show_tasks")
    else:
        bot.send_message(user_id, "Некорректный номер задачи. Пожалуйста, укажите существующий номер.")


@bot.message_handler(commands=['show_tasks'])
def show_tasks(message: Message) -> None:
    """Выводит все текущие задачи пользователя"""
    user_id: int = message.chat.id

    message_text = "Ваши задачи:\n"
    for i, task in enumerate(tasks, start=1):
        message_text += f"{i}. {task[0]} - {task[1]}\n"

    bot.send_message(user_id, message_text)


if __name__ == '__main__':
    bot.infinity_polling()
