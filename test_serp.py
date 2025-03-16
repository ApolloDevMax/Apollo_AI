import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

# Варианты поисковых запросов
search_queries = [
    "Fastest ways to make $100 online in 2025",
    "No investment online earning methods that pay instantly",
    "Legit ways to earn $100 quickly in 2025",
    "Best online gigs to make $100 fast",
    "Highest paying microtasks online"
]

for query in search_queries:
    print(f"\n🔍 Поиск: {query}\n")

    # Настройки запроса
    params = {
        "q": query,
        "location": "United States",
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }

    # Делаем запрос
    search = GoogleSearch(params)
    results = search.get_dict()

    # Выводим 3 результата
    for i, result in enumerate(results.get("organic_results", [])[:3], 1):
        print(f"{i}. {result['title']}")
        print(f"   🔗 {result['link']}\n")
