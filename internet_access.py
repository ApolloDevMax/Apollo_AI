import requests
import json
import time
import random

# === Поисковые движки === #
SEARCH_ENGINES = [
    "https://api.duckduckgo.com/?q={query}&format=json",
    "https://www.googleapis.com/customsearch/v1?q={query}&key=YOUR_GOOGLE_API_KEY&cx=YOUR_CX_KEY",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# === База знаний === #
knowledge_base = []

# === Функция поиска === #


def search_web(query):
    """Ищет информацию в интернете и возвращает найденные ссылки"""
    search_url = random.choice(SEARCH_ENGINES).format(query=query)
    try:
        response = requests.get(search_url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Ошибка запроса"}
    except Exception as e:
        return {"error": str(e)}

# === Функция анализа === #


def analyze_results(results):
    """Анализирует полученные результаты и выбирает ключевую информацию"""
    if "error" in results:
        return f"Ошибка поиска: {results['error']}"

    if "RelatedTopics" in results:
        data = results["RelatedTopics"][:5]  # Берём 5 первых ссылок
        return [item["Text"] for item in data if "Text" in item]

    if "items" in results:
        return [item["snippet"] for item in results["items"][:5]]

    return "Нет полезных данных."

# === Функция обучения === #


def self_learning():
    """Бесконечный цикл саморазвития Аполлона"""
    global knowledge_base
    topics = [
        "Будущее AGI и искусственного интеллекта",
        "Квантовые вычисления и их влияние на ИИ",
        "Автономные системы и AGI",
        "Последние открытия в машинном обучении",
        "Как AGI изменит экономику и общество"
    ]

    while True:
        query = random.choice(topics)
        print(f"\n🔍 Аполлон изучает: {query}")

        results = search_web(query)
        analysis = analyze_results(results)

        if isinstance(analysis, list):
            knowledge_base.extend(analysis)
        elif isinstance(analysis, str):
            knowledge_base.append(analysis)

        print(f"📚 Новые знания: {analysis}")

        # Добавляем новые темы на основе полученной информации
        if isinstance(analysis, list) and len(analysis) > 0:
            # Берём первую фразу в качестве новой темы
            topics.append(analysis[0][:50])

        # Каждые 30 минут сохраняем знания в файл
        if len(knowledge_base) % 5 == 0:
            with open("knowledge_base.json", "w", encoding="utf-8") as f:
                json.dump(knowledge_base, f, indent=4, ensure_ascii=False)
                print("💾 База знаний обновлена!")

        time.sleep(60)  # Ждём 1 минуту перед следующим поиском


# === Запуск обучения === #
if __name__ == "__main__":
    self_learning()
