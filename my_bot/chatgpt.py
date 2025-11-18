# chatgpt.py
import openai
from config import OPENAI_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

openai.api_key = OPENAI_API_KEY


def ask(prompt: str) -> str:
    """
    Отправляем запрос к LLM и возвращаем только текст ответа.
    """
    response = openai.chat.completions.create(   # ← обновлённый вызов
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # В ответе лежит объект `choices[0].message.content`
    return response.choices[0].message.content.strip()
