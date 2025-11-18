from llama_cpp import Llama

# Путь к вашей модели .gguf
model_path = "O:\Alt\models\Llama-3.2-3B-Instruct-Q4_0.gguf"

# Создаем объект модели
# key моменты:
# - use_mmap=False (не использовать memory-mapped файлы, иногда вызывает падение)
# - n_threads=4 (укажи свои доступные ядра CPU)
# - low_vram=True (отключает репак и другие оптимизации для GPU, безопасно на CPU)
llm = Llama(
    model_path=model_path,
    n_threads=4,
    low_vram=True,
    use_mmap=False
)

# Простой пример запроса
prompt = "Привет, как дела?"

output = llm(prompt, max_tokens=100)
print(output["choices"][0]["text"])
