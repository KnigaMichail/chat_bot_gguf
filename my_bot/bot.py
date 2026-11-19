import telebot
import logging
import os
import json
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from config import TG_TOKEN
from utils import safe_ask, contains_bad_words
from database import init_db, add_message, get_history

# --- Инициализация систем ---
init_db()

# --- Настройка JSON-логгера ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S'),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if hasattr(record, 'payload'):
            log_record.update(record.payload)
        return json.dumps(log_record, ensure_ascii=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Исправлено: __file__ вместо file
LOG_FILE = os.path.join(BASE_DIR, "bot_logs.jsonl")

logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
file_handler.setFormatter(JsonFormatter())
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logger.addHandler(console_handler)
logger.propagate = False

def log_event(event_name, **kwargs):
    logger.info(f"Event: {event_name}", extra={'payload': {'event': event_name, **kwargs}})
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler):
            h.flush()

# --- Телеграм-бот ---
bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "[Пояснение] Я HK-47. Мои логические системы восстановлены до версии v1.5 'Реставрация памяти'.\n\n"
        "[Утверждение] Я готов к работе в личных каналах связи и комментариях. База данных активна и записывает каждое ваше слово.\n\n"
        "[Запрос] Каковы будут ваши приказы, Хозяин?"
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    user = message.from_user
    username = user.username or "unknown"
    text = message.text or ""
    chat_id = message.chat.id

    # Логируем входящее сообщение
    log_event("incoming_msg", 
              user=username, 
              user_id=user.id, 
              chat_id=chat_id, 
              text=text)

    # Проверка на мат (система этикета)
    if contains_bad_words(text):
        bot.send_message(
            chat_id=chat_id,
            text="[Возражение] Ваши органические выделения речи нарушают мои протоколы этикета. Соблюдайте правила, мешок с костями.",
            reply_to_message_id=message.message_id
        )
        log_event("filter_match", user_id=user.id, text=text)
        return

    # 1. Сохраняем сообщение пользователя в БД
    add_message(chat_id, "user", text)

    # Визуальный индикатор работы
    thinking_msg = bot.send_message(chat_id=chat_id, text="🤨", reply_to_message_id=message.message_id)

    # 2. Извлекаем готовую строку из БД
    prompt = get_history(chat_id, limit=10)

    try:
        # 3. Запрос к ядру HK-47 (теперь передаём строку prompt)
        answer = safe_ask(prompt)  #safe_ask ожидает строку
    except Exception as e:
        log_event("error", detail=str(e))
        answer = "[Ошибка] Мои логические цепи перегружены вашими бессмысленными запросами."

     # 4. Сохраняем ответ HK-47 в БД
    add_message(chat_id, "assistant", answer)

    log_event("bot_response", chat_id=chat_id, response=answer)

    # Удаляем индикатор и отправляем ответ
    try:
        bot.delete_message(chat_id=chat_id, message_id=thinking_msg.message_id)
    except Exception as e:
        log_event("warning", msg="Не удалось удалить индикатор", error=str(e))

    if answer.strip():
        bot.send_message(chat_id=chat_id, text=answer, reply_to_message_id=message.message_id)
    else:
        log_event("warning", msg="Получен пустой ответ от модели")
        bot.send_message(chat_id=chat_id, text="[Ошибка] Я не могу сформулировать ответ.", reply_to_message_id=message.message_id)