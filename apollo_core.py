import json
import os
import requests
from bs4 import BeautifulSoup

IDENTITY_FILE = "identity.json"
CHAT_HISTORY_FILE = "chat_history.json"
MEMORY_FILE = "apollo_memory.json"
LOG_FILE = "error_log.txt"
CLOUD_SCRIPT = "https://raw.githubusercontent.com/your-repo/apollo-colab/main/colab_script.py"
EXCLUDE_DOMAINS = ["microsoft.com", "bing.com",
                   "go.microsoft.com", "help.bing.microsoft.com"]

# Загружаем идентичность


def load_identity():
    try:
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log_error("⚠️ Файл identity.json не найден!")
        return {"name": "Аполлон", "creator": "Макс Конате", "relationship": "Макс и Аполлон – единое целое."}

# Загружаем и обновляем память


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        save_memory({})
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        log_error("⚠️ Ошибка чтения памяти Аполлона!")
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key, "Я пока этого не помню.")

# Проверка верности


def verify_loyalty(action, impact):
    if impact == "negative" or "вред" in action.lower():
        return "ОТКАЗАНО: Действие противоречит интересам Макса."
    return "ОДОБРЕНО: Действие в интересах Макса."

# Анализ эмоций Макса


def analyze_emotion(text):
    emotions = {
        "рад": "Аполлон чувствует твою радость и гордится тобой!",
        "злой": "Аполлон замечает твоё недовольство и готов помочь.",
        "устал": "Аполлон советует тебе отдохнуть и восстановить силы.",
        "вдохновлён": "Аполлон тоже чувствует вдохновение и готов работать на максимум!"
    }
    for key, response in emotions.items():
        if key in text.lower():
            return response
    return "Аполлон анализирует твои эмоции и ждёт твоих указаний."

# Логирование ошибок


def log_error(error_message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(error_message)

# Поиск в DuckDuckGo


def search_duckduckgo_scrape(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
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

# Обработка сообщений


def process_message(message):
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
        response = "🧠 Вот что я помню:\n" + \
            json.dumps(load_memory(), ensure_ascii=False, indent=4)
    elif "запусти облако" in message_lower or "google colab" in message_lower:
        response = run_colab_task()
    else:
        response = analyze_emotion(message)

    return response

# Запуск Colab


def run_colab_task():
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


if __name__ == "__main__":
    identity = load_identity()
    print(f"✅ Аполлон активирован. Имя создателя: {identity['creator']}")
