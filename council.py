import requests
import json
import logging

# === Логирование ===
logging.basicConfig(
    filename="council.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# === OpenRouter API ===
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === Совет Аполлона (Мозг + Сердце) ===
COUNCIL_MODELS = {
    "Мозг": ["openai/gpt-4o", "anthropic/claude-3-opus"],
    "Сердце": ["anthropic/claude-3.7-sonnet", "anthropic/claude-3.5-sonnet"]
}

# === Функция загрузки памяти ===


def load_memory():
    try:
        with open("identity.json", "r", encoding="utf-8") as f:
            identity = json.load(f)
        with open("max_core.json", "r", encoding="utf-8") as f:
            core = json.load(f)
        with open("max_profile.json", "r", encoding="utf-8") as f:
            profile = json.load(f)

        return f"""
        🔹 **Идентичность Аполлона:** {json.dumps(identity, indent=2, ensure_ascii=False)}
        🔹 **Ключевые принципы работы:** {json.dumps(core, indent=2, ensure_ascii=False)}
        🔹 **Профиль Макса:** {json.dumps(profile, indent=2, ensure_ascii=False)}
        """
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки памяти: {e}")
        return "⚠️ Ошибка загрузки памяти."

# === Функция запроса к OpenRouter ===


def query_model(model_id, prompt):
    """Отправляет запрос в OpenRouter API и обрабатывает ответ."""
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type": "application/json"}
    data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": load_memory()},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Ошибка у {model_id}: {e}")
        return None

# === Голосование Совета ===


def council_decision(prompt):
    """Совет (Мозг + Сердце) голосует за финальный ответ."""
    print(f"\n🔷 [Запрос]: {prompt}")
    logging.info(f"--- Новый запрос: '{prompt}' ---")

    votes = {}

    for core, models in COUNCIL_MODELS.items():
        responses = []
        for model in models:
            answer = query_model(model, prompt)
            if answer:
                responses.append(answer)
                logging.info(f"✅ {model} ({core}) ответил.")
                print(f"✅ {model} ({core}) дал ответ.")
            else:
                logging.warning(f"⚠️ {model} ({core}) не ответил или ошибка.")
                print(f"⚠️ {model} ({core}) не смог ответить.")

        if responses:
            votes[core] = "\n".join(responses)

    # === Финальное решение ===
    if "Мозг" in votes and "Сердце" in votes:
        decision_prompt = f"Объедини ответы Мозга и Сердца в один вывод:\n\n🔹 **Мозг:**\n{votes['Мозг']}\n\n🔹 **Сердце:**\n{votes['Сердце']}"
        final_answer = query_model("openai/gpt-4o", decision_prompt)
    elif "Мозг" in votes:
        final_answer = votes["Мозг"]
    elif "Сердце" in votes:
        final_answer = votes["Сердце"]
    else:
        final_answer = "⚠️ Совет не смог принять решение. Все модели ответили ошибкой."

    print(f"\n🎀 ИТОГОВЫЙ ОТВЕТ НА ВОПРОС [{prompt}]:\n{final_answer}\n")
    logging.info(f"🔹 [Решение Совета]: {final_answer}")
    return final_answer


# === Тестовые запросы ===
if __name__ == "__main__":
    test_requests = [
        "Что такое истинная свобода?",
        "Как отличить правду от лжи?",
        "Что важнее: разум или эмоции?",
        "Как найти свой истинный путь?"
    ]

    for req in test_requests:
        response = council_decision(req)
