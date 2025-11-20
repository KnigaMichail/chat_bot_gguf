# local_gpt.py
import os
from pathlib import Path
import logging

# Путь к .gguf-файлу
MODEL_PATH = Path(r"O:\Alt\models\Llama-3.2-3B-Instruct-Q4_0.gguf")

try:
    from llama_cpp import Llama
except Exception as exc:
    raise RuntimeError(
        "Не удалось импортировать llama-cpp-python. Убедитесь, что пакет установлен."
    ) from exc


class LocalGPT:
    def __init__(self, model_path: Path):
        self.logger = logging.getLogger(__name__)

        # Создаём объект модели
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=4096,
            n_threads=8,     # поставь сколько ядер хочешь
            n_batch=512,
            verbose=False
        )

        self.logger.info(f"Модель загружена из {model_path}")

    def ask(self, prompt: str, max_tokens: int = 300):
        # --- ЧАТ-ШАБЛОН ДЛЯ LLAMA-3.2 ---
        chat_prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>\n"
            "Ты — полезный ассистент, отвечающий понятно и по делу.\n"
            "<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"{prompt}\n"
            "<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n"
        )

        # --- ВЫЗОВ МОДЕЛИ ---
        response = self.llm(
            chat_prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["<|eot_id|>"]
        )

        return response["choices"][0]["text"].strip()


# --- ЕДИНСТВЕННЫЙ ЭКЗЕМПЛЯР МОДЕЛИ ---
local_gpt = LocalGPT(MODEL_PATH)


def ask(prompt: str) -> str:
    """Обёртка – делаем запрос к локальной модели."""
    return local_gpt.ask(prompt)