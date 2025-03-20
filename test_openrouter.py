import requests

# Подставь свой API-ключ OpenRouter
API_KEY = "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"

# Все 11 моделей
MODELS = [
    "deepseek/deepseek-r1:free",
    "nvidia/llama-3.1-nemotron-70b-instruct:free",
    "deepseek/deepseek-chat:free",
    "qwen/qwen2.5-vl-72b-instruct:free",
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "sophosympatheia/rogue-rose-103b-v0.2:free",
    "nousresearch/deephermes-3-llama-3-8b-preview:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-nemo:free"
]

PROMPT = "Ты — утка, но не простая, а тайный агент под прикрытием. У тебя есть одно задание: проникнуть на вечеринку миллионеров и украсть их главный секрет — рецепт идеального блинчика. Как ты это сделаешь?"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Запускаем тест для каждой модели
for model in MODELS:
    print(f"🚀 Тест модели {model}...")

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты умный ИИ с богатым воображением."},
            {"role": "user", "content": PROMPT}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=data)
        result = response.json()

        if "choices" in result and result["choices"]:
            print(
                f"🔹 {model} ответил:\n{result['choices'][0]['message']['content']}\n")
        else:
            print(f"⚠️ {model} не дал ответ.\n")

    except Exception as e:
        print(f"❌ Ошибка при запросе к {model}: {e}\n")
