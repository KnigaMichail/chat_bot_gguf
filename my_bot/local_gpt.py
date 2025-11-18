# local_gpt.py
import os
from pathlib import Path
import logging

# Путь к .gguf‑файлу (обратите внимание на двойные обратные слэши!)
MODEL_PATH = Path(r"O:\Alt\models\Llama-3.2-3B-Instruct-Q4_0.gguf")

# Если хотите использовать CUDA + Torch, установите пакет `llama-cpp-python[torch]`
USE_TORCH = False          # оставьте False – если у вас нет GPU / не хотите тратить память

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
            n_ctx=2048,                     # контекст‑окно (можно уменьшить до 2048)
            n_threads=4,       # кол‑во потоков
            # Если хотите ускорить на GPU: n_gpu_layers=1
        )
        self.logger.info(f"Модель загружена из {model_path}")

    def ask(self, prompt: str, max_tokens: int = 200) -> str:
        """Генерируем ответ."""
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1.0,
            repeat_penalty=1.2,
            stop=None,
        )
        # Внутри `response` ключ `choices[0]["text"]`
        return response["choices"][0]["text"].strip()


# Создаём единственный экземпляр, чтобы модель загружалась один раз
local_gpt = LocalGPT(MODEL_PATH)


def ask(prompt: str) -> str:
    """Обёртка – просто делаем запрос к локальной модели."""
    return local_gpt.ask(prompt)
