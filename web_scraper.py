import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")


def search_google(query):
    """
    Выполняет поиск в Google через SerpAPI (или Google Custom Search API в будущем).
    """
    if not API_KEY:
        print("❌ Ошибка: API-ключ не найден в .env")
        return []

    print(f"🔍 Ищу информацию: {query}...")
    url = f"https://serpapi.com/search.json?q={query}&api_key={API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "organic_results" not in data:
            print("⚠️ Нет результатов. Возможно, исчерпан лимит запросов.")
            return []

        top_results = []
        for result in data["organic_results"][:5]:
            title = result.get("title", "Без названия")
            link = result.get("link", "")
            snippet = result.get("snippet", "")
            top_results.append(
                {"title": title, "link": link, "snippet": snippet})

        print(f"✅ Найдено {len(top_results)} результатов.")
        save_results(query, top_results)
        return top_results
    else:
        print("⚠️ Ошибка поиска!")
        return []


def save_results(query, results):
    """
    Сохраняет результаты поиска в memory.json для последующего использования.
    """
    memory_file = "memory.json"
    if os.path.exists(memory_file):
        with open(memory_file, "r", encoding="utf-8") as file:
            memory_data = json.load(file)
    else:
        memory_data = {}

    memory_data[query] = results
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(memory_data, file, ensure_ascii=False, indent=4)
    print("💾 Данные сохранены в память.")


if __name__ == "__main__":
    query = input("Введите запрос: ")
    results = search_google(query)
    for idx, res in enumerate(results, start=1):
        print(f"{idx}. {res['title']} ({res['link']})")
