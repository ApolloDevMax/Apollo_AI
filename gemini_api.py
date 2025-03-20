import requests

# === 🚀 Настройки API ===
GEMINI_API_KEY = "AIzaSyA1Nn3_uji7OusLGfd57JrTn4cYZdLPTm4"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"


def ask_gemini(prompt):
    """
    Отправляет запрос в Gemini API и получает ответ.
    :param prompt: Строка с вопросом или командой для AI.
    :return: Ответ модели или сообщение об ошибке.
    """
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=data, headers=headers)
        response.raise_for_status()  # Проверяем на ошибки HTTP

        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return f"❌ Ошибка структуры ответа: {result}"

    except requests.exceptions.RequestException as e:
        return f"❌ Ошибка сети: {str(e)}"
