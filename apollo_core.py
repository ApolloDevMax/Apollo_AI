import json
import os
import requests
import subprocess
from bs4 import BeautifulSoup
from memory import Memory
from storage import NewsStorage  # Хранилище новостей

# ==============================
# 🔥 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ==============================

IDENTITY_FILE = "identity.json"
MEMORY_FILE = "apollo_memory.json"
LOG_FILE = "error_log.txt"
NEWS_API_KEY = "d8118941edfb433290e76fb6bc96df31"  # 🔑 Замени на свой API-ключ!
EXCLUDE_DOMAINS = ["microsoft.com", "bing.com", "go.microsoft.com"]

memory = Memory()
news_storage = NewsStorage()

# ==============================
# 🔥 ВСТРОЕННАЯ САМООБУЧАЕМОСТЬ
# ==============================

SELF_IMPROVEMENT_SCRIPT = "self_improvement_loop.py"
PROGRESS_VISUALIZER_SCRIPT = "progress_visualizer.py"


def run_self_improvement():
    """Запускает процесс саморазвития Аполлона."""
    print("🚀 Аполлон запускает цикл саморазвития...")
    subprocess.run(["python", SELF_IMPROVEMENT_SCRIPT])


def show_progress():
    """Отображает прогресс Аполлона."""
    print("📊 Показываю прогресс...")
    subprocess.run(["python", PROGRESS_VISUALIZER_SCRIPT])

# ==============================
# 🔥 АПОЛЛОН: ЛИЧНОСТЬ И ПАМЯТЬ
# ==============================


def load_json(filename, default_value):
    """ Загружаем JSON или создаём новый. """
    if not os.path.exists(filename):
        save_json(filename, default_value)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_error(f"⚠ Ошибка чтения {filename}!")
        return default_value


def save_json(filename, data):
    """ Сохраняем JSON. """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_identity():
    """ Загружаем личность. """
    return load_json(IDENTITY_FILE, {"name": "Аполлон", "creator": "Макс Конате"})


def remember(key, value):
    """ Добавляем информацию в память. """
    memory.add_to_memory(key, value, "long_term")


def recall(key):
    """ Достаём из памяти. """
    return memory.get_from_memory(key) or "❌ Не найдено."

# ==============================
# 🔥 АНАЛИЗ ТЕКСТА
# ==============================


class TextAnalyzer:
    def extract_main_idea(self, text):
        """Извлекает основную идею из текста."""
        sentences = text.split(". ")
        if len(sentences) > 2:
            return f"📌 Главное: {sentences[0]}... {sentences[1]}"
        return f"📌 Ключевая идея: {text}"

    def summarize_article(self, url):
        """Анализирует статью по URL."""
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                full_text = " ".join([p.get_text() for p in paragraphs])
                return self.extract_main_idea(full_text)
            return "⚠ Не удалось загрузить статью."
        except Exception as e:
            return f"⚠ Ошибка при анализе: {str(e)}"


text_analyzer = TextAnalyzer()

# ==============================
# 🔥 НОВОСТИ ИЗ API
# ==============================


def fetch_news():
    """ Получает новости через API. """
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            news_list = []
            for article in data["articles"]:
                title = article["title"]
                source = article["source"]["name"]
                url = article["url"]
                if news_storage.add_news(title, source, url):
                    news_list.append(f"📰 {title} - {source}\n🔗 {url}")
            return "\n".join(news_list) if news_list else "✅ Нет новых новостей."
        else:
            return f"❌ Ошибка API: {data['message']}"
    except Exception as e:
        log_error(f"❌ Ошибка загрузки новостей: {str(e)}")
        return "❌ Ошибка при загрузке новостей."

# ==============================
# 🔥 ОБРАБОТКА СООБЩЕНИЙ
# ==============================


def process_message(message):
    """ Обрабатывает команды пользователя. """
    message_lower = message.lower()
    if "как тебя зовут" in message_lower or "кто ты" in message_lower:
        identity = load_identity()
        return f"Меня зовут {identity['name']}. Я союзник {identity['creator']}!"
    elif "новости" in message_lower:
        return fetch_news()
    elif "анализируй себя" in message_lower:
        run_self_improvement()
        return "🛠 Запустил процесс саморазвития."
    elif "покажи прогресс" in message_lower:
        show_progress()
        return "📊 Отображаю прогресс Аполлона."
    elif "поиск" in message_lower:
        query = message.replace("поиск", "").strip()
        return "🔎 Найденные ссылки:\n" + "\n".join(search_duckduckgo(query))
    elif "проанализируй" in message_lower:
        url = message.replace("проанализируй", "").strip()
        return text_analyzer.summarize_article(url)
    else:
        return "🤖 Я пока не знаю, что ответить."

# ==============================
# 🔥 ИНТЕРАКТИВНЫЙ ЧАТ С АПОЛЛОНОМ
# ==============================


if __name__ == "__main__":
    identity = load_identity()
    print(f"✅ Аполлон активирован. Имя создателя: {identity['creator']}\n")

    while True:
        user_input = input("🟢 Введите команду: ").strip().lower()

        if user_input in ["выход", "exit", "quit"]:
            print("👋 Завершаю работу...")
            break

        response = process_message(user_input)
        print(response)
