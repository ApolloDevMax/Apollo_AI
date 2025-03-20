import requests
import random

# 🔥 OpenRouter API Key (замени, если надо)
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# 🔥 8 ИИ-моделей (подключены к OpenRouter)
MODELS = {
    "gemini": "google/gemini-2.0-pro-exp-02-05:free",  # Google Gemini 2.0 Pro
    # DeepSeek R1 (логика, анализ, reasoning)
    "deepseek": "deepseek-ai/deepseek-r1",
    # Llama 3.3 70B (общение, языковые модели)
    "llama": "meta-llama/llama-3.3-70b",
    # Qwen2.5 Coder (программирование, автоматизация)
    "qwen_coder": "qwen/qwen2.5-coder-32b",
    # R1 Distill Qwen (математика, точные вычисления)
    "r1_distill": "r1-distill/qwen-32b",
    # DeepSeek R1 Zero (глубокий reasoning, многозадачность)
    "deepseek_zero": "deepseek-ai/deepseek-r1-zero",
    # Qwen2.5 72B (сложные вычисления, кодинг)
    "qwen_72b": "qwen/qwen2.5-72b-instruct",
    # Sonar Deep Research (финансы, аналитика)
    "sonar": "perplexity/sonar-deep-research"
}

# 🔍 Функция поиска в Wikipedia API


def wikipedia_search(query):
    """
    Ищет информацию в Wikipedia API и выдаёт статьи с ссылками.
    """
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "query" in data and "search" in data["query"]:
            results = []
            for article in data["query"]["search"][:5]:  # Берём 5 статей
                title = article["title"]
                pageid = article["pageid"]
                snippet = article["snippet"]  # Короткий текст из статьи
                # Прямая ссылка
                link = f"https://en.wikipedia.org/?curid={pageid}"

                results.append(f"📌 {title}\n🔗 {link}\n📝 {snippet}\n")

            return results if results else ["❌ Wikipedia не нашла результатов."]

    except requests.exceptions.RequestException as e:
        return [f"❌ Ошибка Wikipedia API: {str(e)}"]

# 🔥 Функция для запроса к OpenRouter AI (с выбором модели)


def ask_openrouter(prompt, model="gemini", max_tokens=1000):
    """
    Отправляет запрос к OpenRouter AI и выбирает модель в зависимости от задачи.
    """
    if model not in MODELS:
        model = "gemini"  # По умолчанию используем Gemini 2.0

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODELS[model],  # Выбираем модель из списка
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "❌ Ошибка: Пустой ответ от OpenRouter."

    except requests.exceptions.RequestException as e:
        return f"❌ Ошибка запроса OpenRouter: {str(e)}"


# 🔥 Тестируем API (с 8 моделями)
if __name__ == "__main__":
    test_query = "Artificial Intelligence"

    print("\n🔹 Wikipedia результаты:")
    wiki_results = wikipedia_search(test_query)
    for res in wiki_results:
        print(res)

    print("\n🤖 Анализ AI (Gemini):")
    analysis_gemini = ask_openrouter(
        f"Анализируй статью из Wikipedia о {test_query} и сделай выводы.", model="gemini")
    print(analysis_gemini)

    print("\n🤖 Анализ AI (DeepSeek R1 Zero):")
    analysis_deepseek = ask_openrouter(
        f"Анализируй статью из Wikipedia о {test_query} и сделай выводы.", model="deepseek_zero")
    print(analysis_deepseek)
