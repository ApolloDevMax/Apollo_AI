import requests
import json
import time
import logging

# 🔥 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

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


# 📌 **Список моделей для СЕРДЦА**
HEART_MODELS = {
    "Claude 3.7 Sonnet": "anthropic/claude-3.7-sonnet",
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet"
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


def query_heart_model(model_name, model_id, prompt, memory_context):
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
    try:
        response = requests.post(url, json=data, headers=headers, timeout=20)
        response_time = round(time.time() - start_time, 2)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            return model_name, answer, response_time
        else:
            return model_name, f"❌ Ошибка: {response.text}", response_time
    except requests.exceptions.RequestException as e:
        return model_name, f"❌ Ошибка: {e}", 0

# 🚀 **Запуск тестирования**


def test_heart():
    print("\n🔹 **Тестирование модуля \"СЕРДЦЕ\" с загруженной памятью...**\n")
    memory_context = load_memory()

    for prompt in TEST_PROMPTS:
        print(f"💬 **Вопрос:** {prompt}\n")
        for name, model_id in HEART_MODELS.items():
            result = query_heart_model(name, model_id, prompt, memory_context)
            logging.info(f"✅ {result[0]} ответил за {result[2]} сек.")
            print(
                f"💖 **{result[0]}** (⏱ {result[2]} сек):\n{result[1]}\n{'-'*50}")
        print("\n")


if __name__ == "__main__":
    test_heart()
