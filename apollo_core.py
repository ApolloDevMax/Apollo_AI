import json
import logging
import requests
from datetime import datetime

# 🔥 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# 🔑 API-ключ для OpenRouter
API_KEY = "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"

# 🧠 Подключение моделей "Мозга" (Core AI)
BRAIN_MODELS = {
    "GPT-4o": "openai/gpt-4o",
    "Claude 3 Opus": "anthropic/claude-3-opus"
}

# 🎯 Вопрос для тестирования
TEST_QUESTION = "Какова роль ИИ в будущем человечества?"


def query_model(model_name, model_id, prompt):
    """Запрашивает ответ у модели через OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Ошибка у {model_name}: {e}")
        return f"❌ Ошибка запроса к {model_name}"
    except KeyError:
        logging.error(f"❌ Ошибка в JSON-ответе от {model_name}")
        return f"❌ Ошибка формата ответа от {model_name}"


def test_brain_models():
    """Тестирует все модели "Мозга" """
    print("🔹 Тестирование модуля \"МОЗГ\" с загруженной памятью...\n")

    for model_name, model_id in BRAIN_MODELS.items():
        print(f"🧠 **{model_name}** ({datetime.now().strftime('%H:%M:%S')})")
        response = query_model(model_name, model_id, TEST_QUESTION)
        print(response)
        print("-" * 80)


# 📌 Запуск тестирования
if __name__ == "__main__":
    test_brain_models()
