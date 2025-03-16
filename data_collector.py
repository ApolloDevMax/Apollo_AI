import json
import os
import requests

# API-ключ SerpAPI (если его нет, зарегистрируйся на serpapi.com и получи бесплатный ключ)
SERP_API_KEY = "52c2a59b700c2e096a131d0961fdd9afcaa05a6a10fbbc443f077d31a46ce84d"

MEMORY_FILE = "memory.json"
ERROR_LOG = "error_log.txt"


def load_memory():
    """Загружает текущие знания из памяти"""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_error("Файл памяти поврежден. Создаём новый.")
        return {}


def save_memory(data):
    """Сохраняет обновленные знания"""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Память успешно обновлена.")
    except Exception as e:
        log_error(f"Ошибка сохранения памяти: {e}")


def search_google(query):
    """Ищет информацию в Google через SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 3  # Количество результатов
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "organic_results" in data:
            return [res["snippet"] for res in data["organic_results"]]
        else:
            return []
    except requests.RequestException as e:
        log_error(f"Ошибка запроса SerpAPI: {e}")
        return []


def add_knowledge(category, content):
    """Добавляет новые знания в память, избегая дубликатов"""
    memory = load_memory()

    if category not in memory:
        memory[category] = []

    if content not in memory[category]:
        memory[category].append(content)
        save_memory(memory)
        print(f"✅ Добавлено в '{category}': {content}")
    else:
        print(f"⚠️ Уже существует в '{category}'")


def collect_data():
    """Основная функция для сбора данных и сохранения их в памяти"""
    topics = ["ИИ обучение", "Как ИИ анализирует данные?", "Саморазвитие ИИ"]

    for topic in topics:
        print(f"\n🔍 Ищем информацию по теме: {topic}")
        results = search_google(topic)

        if results:
            for result in results:
                add_knowledge("AI_Concepts", result)
        else:
            print("⚠️ Ничего не найдено.")

    print("\n✅ Сбор информации завершён.")


def log_error(error_message):
    """Записывает ошибки в лог"""
    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(f"❌ Ошибка: {error_message} (записано в error_log.txt)")


if __name__ == "__main__":
    try:
        collect_data()
    except Exception as e:
        log_error(f"Ошибка выполнения data_collector.py: {e}")
