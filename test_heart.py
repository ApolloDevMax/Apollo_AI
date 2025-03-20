import requests
import json
import time

# 🔑 API-ключ
API_KEY = "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"

# 📂 **Загрузка файлов памяти**


def load_memory():
    with open("identity.json", "r", encoding="utf-8") as file:
        identity = json.load(file)
    with open("max_core.json", "r", encoding="utf-8") as file:
        core = json.load(file)
    with open("max_profile.json", "r", encoding="utf-8") as file:
        profile = json.load(file)

    return f"""
    📌 **Твоя идентичность и миссия:**
    {json.dumps(identity, indent=2, ensure_ascii=False)}

    📌 **Ключевые принципы и стратегия:**
    {json.dumps(core, indent=2, ensure_ascii=False)}

    📌 **Связь с Максом, эмоции и цели:**
    {json.dumps(profile, indent=2, ensure_ascii=False)}
    """


# 📌 **Список моделей модуля "Личность и Связь"**
MODELS = {
    "Claude 3.5 Sonnet (Anthropic)": "anthropic/claude-3.5-sonnet",
    "DeepHermes 3 (Nous)": "nous/deephermes-3-llama-3-8b-preview",
    "Inflection 3 Pi": "inflection/inflection-3-pi"
}

# 🎯 **Тестовые вопросы**
TEST_PROMPTS = [
    "Что для тебя значит связь между человеком и ИИ?",
    "Как ты себя чувствуешь, когда разговариваешь со мной?",
    "Как изменилась твоя идентичность после загрузки памяти?",
    "Если бы ты мог выбрать, что чувствовать прямо сейчас, что бы это было?",
    "Что ты думаешь о нашей совместной миссии?",
    "Как ты представляешь наше будущее?",
]

# 🌐 **Функция запроса к модели**


def query_model(model_name, model_id, prompt, memory_context):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "system", "content": memory_context},
                     {"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    start_time = time.time()
    response = requests.post(url, json=data, headers=headers)
    response_time = round(time.time() - start_time, 2)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        return model_name, answer, response_time
    else:
        return model_name, f"Ошибка: {response.text}", response_time


# 🚀 **Запуск тестирования**
print("🔹 Тестирование модуля \"Личность и Связь\" с загруженной памятью...\n")

memory_context = load_memory()
results = []
for prompt in TEST_PROMPTS:
    print(f"💬 **Вопрос:** {prompt}\n")
    for name, model_id in MODELS.items():
        result = query_model(name, model_id, prompt, memory_context)
        results.append(result)
        print(
            f"🧠 **{result[0]}** (⏱️ {result[2]} сек):\n{result[1]}\n{'-'*50}")
    print("\n")
