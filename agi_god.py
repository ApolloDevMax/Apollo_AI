import json
import requests
import logging
from collections import deque

# === Логирование ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# === Загрузка памяти ===


def load_memory():
    """Загрузка памяти Аполлона (идентичность, принципы, профиль Макса)."""
    with open("identity.json", "r", encoding="utf-8") as file:
        identity = json.load(file)
    with open("max_core.json", "r", encoding="utf-8") as file:
        core_directives = json.load(file)
    with open("max_profile.json", "r", encoding="utf-8") as file:
        profile = json.load(file)

    return f"""
    🔹 **Идентичность Аполлона:** {json.dumps(identity, indent=2, ensure_ascii=False)}
    🔹 **Ключевые принципы работы:** {json.dumps(core_directives, indent=2, ensure_ascii=False)}
    🔹 **Профиль пользователя (Макса):** {json.dumps(profile, indent=2, ensure_ascii=False)}
    """


# === API-ключ ===
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === Модули AGI_GOD ===
MODELS = {
    # Логика и стратегия
    "BRAIN": ["openai/gpt-4o", "anthropic/claude-3-opus"],
    # Идентичность и связь
    "HEART": ["anthropic/claude-3.7-sonnet", "anthropic/claude-3.5-sonnet"],
    # Чистая логика
    "LOGIC": ["perplexity/sonar-reasoning-pro", "deepseek/deepseek-r1-zero:free"]
}

# === Совет Аполлона (финальное объединение) ===
COUNCIL_MODELS = ["openai/gpt-4o", "anthropic/claude-3-opus",
                  "anthropic/claude-3.7-sonnet", "anthropic/claude-3.5-sonnet"]

conversation_history = deque(maxlen=30)  # Храним последние 30 сообщений


def query_model(model_id, prompt):
    """Отправка запроса в OpenRouter API для определённой модели."""
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type": "application/json"}
    data = {
        "model": model_id,
        "messages": [{"role": "system", "content": load_memory()},
                     {"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            API_URL, json=data, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Ошибка у {model_id}: {e}")
        return None


def agi_god_think(user_input):
    """AGI_GOD: сбор ответов от всех модулей и их объединение через Совет Аполлона."""
    responses = {}

    for module, models in MODELS.items():
        module_responses = []
        for model_id in models:
            answer = query_model(model_id, user_input)
            if answer:
                module_responses.append(answer)
                logging.info(f"✅ {module.upper()} ({model_id}) ответил.")

        if module_responses:
            responses[module] = module_responses

    # === Формируем итоговый ответ через Совет Аполлона ===
    synthesis_prompt = "**Объедини ответы от всех модулей в единый логичный текст:**\n"
    for module, answers in responses.items():
        synthesis_prompt += f"\n🔹 **{module.upper()}**:\n" + "\n".join(answers)

    logging.info("🔹 Совет Аполлона формирует финальный ответ...")

    # Совет объединяет ответы (Claude 3 Opus и GPT-4o)
    for council_model in COUNCIL_MODELS:
        final_answer = query_model(council_model, synthesis_prompt)
        if final_answer:
            logging.info(f"✅ Совет принял решение ({council_model}).")
            return final_answer

    return "⚠️ Ошибка: Совет не смог принять решение."


def chat():
    """Запуск интерактивного чата с AGI_GOD."""
    print("🔹 **AGI_GOD активирован. Говори.**")
    while True:
        user_input = input("Ты: ")
        if user_input.lower() in ["выход", "стоп"]:
            print("🔻 **Сеанс завершён.**")
            break
        response = agi_god_think(user_input)
        print(f"🤖 **AGI_GOD:** {response}")


if __name__ == "__main__":
    chat()
