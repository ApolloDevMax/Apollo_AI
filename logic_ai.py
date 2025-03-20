import requests
import json

# === Конфигурация моделей ===
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "Sonar Reasoning Pro": "perplexity/sonar-reasoning-pro",
    "DeepSeek R1 Zero": "deepseek/deepseek-r1-zero:free"
}

# === Функция запроса к OpenRouter ===


def ask_model(request, model_id):
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": request}],
        "temperature": 0.5  # Стабильность и логичность ответов
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе к {model_id}: {e}")
        return None

# === Функция работы двух ИИ в связке ===


def logic_analysis(request):
    print(f"\n🔹 [Вопрос]: {request}\n")

    responses = {}
    for name, model in MODELS.items():
        response = ask_model(request, model)
        if response:
            responses[name] = response
            # Обрезаем, чтобы не засорять вывод
            print(f"🔸 [{name}]: {response[:300]}...\n")
        else:
            print(f"❌ [{name}] не ответил.")

    # === Объединение ответов ===
    if len(responses) == 2:
        final_response = f"🧠 **Анализ Sonar Reasoning Pro:** {responses['Sonar Reasoning Pro']}\n\n" \
                         f"🤖 **Анализ DeepSeek R1 Zero:** {responses['DeepSeek R1 Zero']}\n\n" \
                         f"🔷 **Вывод:** {responses['Sonar Reasoning Pro']} {responses['DeepSeek R1 Zero']}"
    else:
        final_response = "⚠️ Один из ИИ не смог ответить, вывод ограничен."

    print(f"\n🔹 [Итоговый ответ]: {final_response}\n")
    return final_response


# === Тестируем связку двух ИИ ===
if __name__ == "__main__":
    test_queries = [
        "Каковы ключевые принципы логического мышления?",
        "Как построить сильную аргументацию?",
        "Почему критическое мышление важно в принятии решений?"
    ]

    for query in test_queries:
        logic_analysis(query)
