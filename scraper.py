import json
import os
import requests
import time
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

MEMORY_FILE = "memory.json"

# Функция загрузки памяти


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Функция сохранения памяти


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Функция проверки, делался ли уже этот запрос


def query_already_searched(query, memory):
    if "Internet_Search" in memory:
        for item in memory["Internet_Search"]:
            if item["query"].lower() == query.lower():
                return True  # Запрос уже выполнялся
    return False

# Функция поиска через SerpAPI


def search_serpapi(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5  # Количество результатов
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = [result["snippet"] for result in data.get(
            "organic_results", []) if "snippet" in result]
        return results if results else ["Нет данных"]
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return ["Ошибка получения данных"]

# Основная функция для поиска новых данных


def run_scraper():
    memory = load_memory()

    # Список тем для исследования
    queries = [
        "новые достижения в искусственном интеллекте",
        "будущее Web3 и блокчейна",
        "как заработать деньги с помощью AI",
        "инновации в автоматизации бизнеса",
        "распределенные вычисления и их потенциал",
        "новые технологии в стартапах",
        "самообучающиеся системы AI"
    ]

    new_data = []
    for query in queries:
        if query_already_searched(query, memory):
            print(f"⏩ Пропускаем, уже искали: {query}")
            continue

        print(f"🔍 Поиск информации: {query}")
        results = search_serpapi(query)

        # Сохраняем в память
        memory.setdefault("Internet_Search", []).append(
            {"query": query, "results": results})
        new_data.append((query, results))

        # Ждём 3 секунды, чтобы избежать ограничения по API
        time.sleep(3)

    if new_data:
        save_memory(memory)
        print("\n✅ Новые данные сохранены!\n")
        for query, results in new_data:
            # Выводим только первые 2 результата
            print(f"🌐 {query}: {results[:2]}...")


if __name__ == "__main__":
    run_scraper()
