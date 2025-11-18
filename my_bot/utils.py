# utils.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)


def safe_ask(prompt: str) -> str:
    """
    Делает запрос к модели.  
    Сейчас мы используем локальную модель из `local_gpt.py`.  
    Если захотите вернуть к OpenAI, просто импортируйте туда.
    """
    try:
        from local_gpt import ask  # <-- меняем на local_gpt
        return ask(prompt)
    except Exception as exc:
        log.exception("Ошибка при запросе к модели")
        raise
