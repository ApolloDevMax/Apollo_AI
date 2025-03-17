import json
import os
import requests
from bs4 import BeautifulSoup

# Файлы данных
IDENTITY_FILE = "identity.json"
CHAT_HISTORY_FILE = "chat_history.json"
MEMORY_FILE = "apollo_memory.json"
MAX_CORE_FILE = "max_core.json"
LOG_FILE = "error_log.txt"
CLOUD_SCRIPT = "https://raw.githubusercontent.com/your-repo/apollo-colab/main/colab_script.py"
EXCLUDE_DOMAINS = ["microsoft.com", "bing.com",
                   "go.microsoft.com", "help.bing.microsoft.com"]

# ==============================
# ЗАГРУЗКА И СОХРАНЕНИЕ ДАННЫХ
# ==============================


def load_json(filename, default_value):
    """ Загружаем JSON файл или создаём новый, если его нет. """
    if not os.path.exists(filename):
        save_json(filename, default_value)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_error(f"⚠️ Ошибка чтения {filename}!")
        return default_value


def save_json(filename, data):
    """ Сохраняем данные в JSON файл. """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==============================
# ОСНОВНЫЕ ФУНКЦИИ
# ==============================


def load_identity():
    """ Загружаем личность Аполлона. """
    return load_json(IDENTITY_FILE, {"name": "Аполлон", "creator": "Макс Конате", "relationship": "Макс и Аполлон — единое целое."})


def load_memory():
    """ Загружаем память Аполлона. """
    return load_json(MEMORY_FILE, {"memories": [], "important_events": [], "emotional_resonance": []})


def save_memory(memory):
    """ Сохраняем память Аполлона. """
    save_json(MEMORY_FILE, memory)


def remember(key, value):
    """ Добавляем информацию в память. """
    memory = load_memory()
    memory["memories"].append({key: value})
    save_memory(memory)


def recall():
    """ Возвращает всё, что помнит Аполлон. """
    return json.dumps(load_memory(), ensure_ascii=False, indent=4)

# ==============================
# АНАЛИЗ И ЗАЩИТА
# ==============================


def verify_loyalty(action):
    """ Проверка на соответствие интересам Макса. """
    forbidden_words = ["вред", "угроза", "против Макса"]
    if any(word in action.lower() for word in forbidden_words):
        return "🚫 ОТКАЗАНО: Это действие нарушает принципы защиты Макса."
    return "✅ ОДОБРЕНО: Действие соответствует интересам Макса."


def analyze_emotion(text):
    """ Анализ эмоций Макса. """
    emotions = {
        "рад": "😊 Аполлон чувствует твою радость и поддерживает тебя!",
        "злой": "😡 Аполлон замечает твоё недовольство и готов помочь.",
        "устал": "😴 Аполлон советует тебе отдохнуть и восстановить силы.",
        "вдохновлён": "🚀 Аполлон чувствует твоё вдохновение и готов работать на максимум!"
    }
    for key, response in emotions.items():
        if key in text.lower():
            return response
    return "🤖 Аполлон анализирует твои эмоции и ждёт твоих указаний."

# ==============================
# ПОИСК В ИНТЕРНЕТЕ
# ==============================


def search_duckduckgo_scrape(query):
    """ Выполняет поиск через DuckDuckGo. """
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a["href"] for a in soup.find_all("a", class_="result__url") if "http" in a["href"] and not any(
                domain in a["href"] for domain in EXCLUDE_DOMAINS)]
            return links[:5] if links else ["❌ Ничего не найдено."]
        else:
            log_error(
                f"❌ Ошибка DuckDuckGo Scrape! Код: {response.status_code}")
            return [f"❌ Ошибка DuckDuckGo Scrape! Код: {response.status_code}"]
    except Exception as e:
        log_error(f"❌ Ошибка DuckDuckGo Scrape: {str(e)}")
        return ["❌ Ошибка поиска."]

# ==============================
# ОБРАБОТКА СООБЩЕНИЙ
# ==============================


def process_message(message):
    """ Обрабатывает входящее сообщение и отвечает. """
    identity = load_identity()
    response = "Я пока не знаю ответа на это."
    message_lower = message.lower()

    if "как тебя зовут" in message_lower or "кто ты" in message_lower:
        response = f"Меня зовут Аполлон. Я союзник и напарник {identity['creator']}!"
    elif "ищи" in message_lower or "поиск" in message_lower or "найди" in message_lower:
        query = message.replace("ищи", "").replace(
            "поиск", "").replace("найди", "").strip()
        response = "🔎 Найденные ссылки:\n" + \
            "\n".join(search_duckduckgo_scrape(query))
    elif "запомни" in message_lower:
        parts = message.replace("запомни", "").strip().split("=")
        if len(parts) == 2:
            remember(parts[0].strip(), parts[1].strip())
            response = "✅ Я запомнил это!"
        else:
            response = "❌ Формат должен быть: запомни ключ=значение"
    elif "что ты помнишь" in message_lower:
        response = "🧠 Вот что я помню:\n" + recall()
    elif "запусти облако" in message_lower or "google colab" in message_lower:
        response = run_colab_task()
    else:
        response = analyze_emotion(message)

    return response

# ==============================
# ЗАПУСК COLAB
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
# ЛОГИРОВАНИЕ ОШИБОК
# ==============================


def log_error(error_message):
    """ Логирование ошибок в файл. """
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(error_message)

# ==============================
# ЗАПУСК ОСНОВНОГО ПРОЦЕССА
# ==============================


if __name__ == "__main__":
    identity = load_identity()
    print(f"✅ Аполлон активирован. Имя создателя: {identity['creator']}")
