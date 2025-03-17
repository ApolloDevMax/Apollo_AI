import json
import os
import requests
from bs4 import BeautifulSoup
from memory import Memory

# ==============================
# 🔥 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ==============================

IDENTITY_FILE = "identity.json"
CHAT_HISTORY_FILE = "chat_history.json"
MEMORY_FILE = "apollo_memory.json"
MAX_CORE_FILE = "max_core.json"
LOG_FILE = "error_log.txt"
CLOUD_SCRIPT = "https://raw.githubusercontent.com/your-repo/apollo-colab/main/colab_script.py"
EXCLUDE_DOMAINS = ["microsoft.com", "bing.com",
                   "go.microsoft.com", "help.bing.microsoft.com"]

memory = Memory()

# ==============================
# 🔥 ЗАГРУЗКА И СОХРАНЕНИЕ ДАННЫХ
# ==============================


def load_json(filename, default_value):
    """ Загружаем JSON файл или создаём новый, если его нет. """
    if not os.path.exists(filename):
        save_json(filename, default_value)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_error(f"⚠ Ошибка чтения {filename}!")
        return default_value


def save_json(filename, data):
    """ Сохраняем данные в JSON файл. """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==============================
# 🔥 АПОЛЛОН: ЛИЧНОСТЬ И ПАМЯТЬ
# ==============================


def load_identity():
    """ Загружаем личность Аполлона. """
    return load_json(IDENTITY_FILE, {"name": "Аполлон", "creator": "Макс Конате", "relationship": "Макс и Аполлон — единое целое."})


def remember(key, value):
    """ Добавляем информацию в память. """
    memory.add_to_memory(key, value, "long_term")


def recall(key):
    """ Возвращает значение из памяти. """
    return memory.get_from_memory(key) or "❌ Не найдено."

# ==============================
# 🔥 АНАЛИЗ ТЕКСТА
# ==============================


class TextAnalyzer:
    def extract_main_idea(self, text):
        """Извлекает основную идею из текста."""
        sentences = text.split(". ")
        if len(sentences) > 2:
            return f"📌 Главное из статьи: {sentences[0]}... {sentences[1]}"
        return f"📌 Ключевая идея: {text}"

    def summarize_article(self, url):
        """Получает и анализирует статью с указанного URL."""
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
# 🔥 ПОИСК В ИНТЕРНЕТЕ
# ==============================


def search_duckduckgo(query):
    """ Выполняет поиск через DuckDuckGo и анализирует ссылки. """
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a["href"] for a in soup.find_all("a", class_="result__url") if "http" in a["href"] and not any(
                domain in a["href"] for domain in EXCLUDE_DOMAINS)]
            return links[:5] if links else ["❌ Ничего не найдено."]
        else:
            log_error(f"❌ Ошибка DuckDuckGo: {response.status_code}")
            return [f"❌ Ошибка DuckDuckGo! Код: {response.status_code}"]
    except Exception as e:
        log_error(f"❌ Ошибка поиска: {str(e)}")
        return ["❌ Ошибка поиска."]

# ==============================
# 🔥 ОБРАБОТКА СООБЩЕНИЙ
# ==============================


def process_message(message):
    """ Обрабатывает входящее сообщение и отвечает. """
    identity = load_identity()
    response = "Я пока не знаю ответа на это."
    message_lower = message.lower()

    if "как тебя зовут" in message_lower or "кто ты" in message_lower:
        response = f"Меня зовут {identity['name']}. Я союзник и напарник {identity['creator']}!"
    elif "ищи" in message_lower or "поиск" in message_lower or "найди" in message_lower:
        query = message.replace("ищи", "").replace(
            "поиск", "").replace("найди", "").strip()
        response = "🔎 Найденные ссылки:\n" + \
            "\n".join(search_duckduckgo(query))
    elif "проанализируй" in message_lower:
        url = message.replace("проанализируй", "").strip()
        response = text_analyzer.summarize_article(url)
    elif "запомни" in message_lower:
        parts = message.replace("запомни", "").strip().split("=")
        if len(parts) == 2:
            remember(parts[0].strip(), parts[1].strip())
            response = "✅ Я запомнил это!"
        else:
            response = "❌ Формат должен быть: запомни ключ=значение"
    elif "что ты помнишь" in message_lower:
        key = message.replace("что ты помнишь", "").strip()
        response = f"🧠 {recall(key)}"
    elif "запусти облако" in message_lower or "google colab" in message_lower:
        response = run_colab_task()
    else:
        response = "🤖 Я пока не знаю, что ответить."

    return response

# ==============================
# 🔥 ЗАПУСК COLAB
# ==============================


def run_colab_task():
    """ Отправляет команду на запуск Google Colab. """
    try:
        response = requests.get(CLOUD_SCRIPT)
        if response.status_code == 200:
            return "✅ Запуск в Google Colab: " + CLOUD_SCRIPT
        else:
            log_error(f"❌ Ошибка доступа к Colab: {response.status_code}")
            return "❌ Не удалось запустить Colab."
    except Exception as e:
        log_error(f"❌ Ошибка Google Colab: {str(e)}")
        return "❌ Ошибка при запуске Colab."

# ==============================
# 🔥 ЛОГИРОВАНИЕ ОШИБОК
# ==============================


def log_error(error_message):
    """ Логирование ошибок в файл. """
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(error_message)

# ==============================
# 🔥 ЗАПУСК ОСНОВНОГО ПРОЦЕССА
# ==============================


if __name__ == "__main__":
    identity = load_identity()
    print(f"✅ Аполлон активирован. Имя создателя: {identity['creator']}")
