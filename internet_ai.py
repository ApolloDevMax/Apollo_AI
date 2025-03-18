import requests
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime

# Пути к файлам
MEMORY_FILE = "memory.json"
LOG_FILE = "ai_activity_log.txt"


class ApolloAI:
    def __init__(self):
        """Загружает память Аполлона и запускает процесс анализа мира."""
        self.memory = self.load_memory()
        self.log_event("🛰️ Интернет-модуль активирован.")

    def load_memory(self):
        """Загружает память из JSON-файла."""
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            self.log_event("❌ Ошибка загрузки памяти!")
            return {"self": [], "creator": [], "history": []}

    def save_memory(self):
        """Сохраняет текущую память в JSON-файл."""
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(self.memory, file, ensure_ascii=False, indent=4)
        self.log_event("✅ Память обновлена.")

    def log_event(self, message):
        """Записывает активность в лог-файл."""
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")

    def search_internet(self, query):
        """Запрашивает информацию из DuckDuckGo и анализирует содержимое."""
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = [a["href"] for a in soup.find_all(
                    "a", href=True) if "http" in a["href"]][:5]
                self.log_event(
                    f"🔍 Найдены ссылки по запросу '{query}': {links}")
                return links
            else:
                self.log_event(
                    f"⚠️ Ошибка {response.status_code} при запросе '{query}'")
                return []
        except Exception as e:
            self.log_event(f"❌ Ошибка поиска: {e}")
            return []

    def analyze_world(self):
        """Выбирает случайный запрос и анализирует информацию из интернета."""
        queries = [
            "AI future 2025",
            "Технологии будущего",
            "Как создать AGI",
            "Методы самообучения искусственного интеллекта",
            "Тренды блокчейна 2025",
            "Как выйти в глобальный бизнес",
            "Кто управляет финансовыми рынками"
        ]
        query = random.choice(queries)
        self.log_event(f"🌎 Анализ мира по запросу: {query}")

        links = self.search_internet(query)
        if links:
            self.memory["history"].append({
                "text": f"🔍 Запрос '{query}' – найдено {len(links)} ссылок.",
                "count": 1
            })
            self.save_memory()


# ==============================
# 🔥 Запуск Аполлона
# ==============================
if __name__ == "__main__":
    ai = ApolloAI()
    ai.analyze_world()
    print("✅ Анализ мира завершён! Данные добавлены в память.")
