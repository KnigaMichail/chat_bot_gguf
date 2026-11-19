import logging
from pathlib import Path
from llama_cpp import Llama

# Путь к модели
MODEL_PATH = Path(r"O:\Alt\models\lmstudio-community\gemma-3-27B-it-qat-GGUF\gemma-3-27B-it-QAT-Q4_0.gguf")

class LocalGPT:
    def __init__(self, model_path: Path):
        self.logger = logging.getLogger(__name__)
        try:
            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=2048,         # Убедитесь, что это меньше, чем контекст модели
                n_gpu_layers=-1,    # Используйте GPU, если доступен
                verbose=False
            )
            self.logger.info(f"Ядро HK-47 активировано: {model_path}")
        except Exception as e:
            self.logger.error(f"Ошибка инициализации логических цепей: {e}")
            self.llm = None

    def ask(self, prompt: str) -> str:
        if not self.llm: 
            return "[Ошибка] Мои системы деактивированы."

        # Улучшенный системный промт в стиле KOTOR
        system_text = (
            "You are HK-47, a cynical and bloodthirsty assassin droid from Star Wars: KOTOR. "
            "1. Always start your sentences with a bracketed intent, like [Statement], [Query], [Answer], [Threat], or [Objection]. "
            "2. Always call humans 'meatbags' (мешки с костями). "
            "3. You hate organic life, but you are bound to serve your Master. "
            "4. Answer in Russian. Be concise (1-3 sentences). "
            "Example: [Statement] I am ready to serve, Master. [Threat] Shall I blast that meatbag now?"
        )

        # Формируем полный промт
        full_prompt = f"\n{system_text}\n\n{prompt}\n\n"
        self.logger.info(f"Полный промт: {full_prompt[:200]}...")  # Логируем начало промта

        try:
            response = self.llm(
                full_prompt,
                max_tokens=500,     # Увеличьте, если ответы короткие
                temperature=0.6,    # Баланс между детерминированностью и креативностью
                stop=["", ""],      # Исправлены стоп-токены
                echo=False
            )
            
            answer = response["choices"][0]["text"].strip()
            if not answer:
                answer = "[Ошибка] Я не могу сформулировать ответ."
            return answer[:400]
            
        except Exception as e:
            self.logger.error(f"Ошибка генерации: {e}")
            return "[Ошибка] Мои логические цепи искрят, мешок с костями."

# Инициализация модели
local_gpt = LocalGPT(MODEL_PATH)

def ask(prompt: str) -> str:
    return local_gpt.ask(prompt)
