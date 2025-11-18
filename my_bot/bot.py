# bot.py
import telebot
from telebot import types

from config import TG_TOKEN
from utils import safe_ask

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Пиши мне, и я буду отвечать GPT‑моделями."
    )


@bot.message_handler(content_types=['text'])
def chat_with_gpt(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        answer = safe_ask(message.text)
    except Exception:
        answer = "Извини, произошла ошибка. Попробуй позже."

    bot.send_message(message.chat.id, answer)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)



