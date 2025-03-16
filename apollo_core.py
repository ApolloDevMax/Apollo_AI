import json
import os
import requests
from bs4 import BeautifulSoup

IDENTITY_FILE = "identity.json"
CHAT_HISTORY_FILE = "chat_history.json"
LOG_FILE = "error_log.txt"  # Логирование ошибок
# Ссылка на код для Google Colab
CLOUD_SCRIPT = "https://raw.githubusercontent.com/your-repo/apollo-colab/main/colab_script.py"

EXCLUDE_DOMAINS = ["microsoft.com", "bing.com",
                   "go.microsoft.com", "help.bing.microsoft.com"]


def load_identity():
    """Загружаем ключевую идентичность Макса и Аполлона."""
    try:
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log_error("⚠️ Файл identity.json не найден!")
        return {"name": "Макс Конате", "role": "Создатель и союзник Аполлона"}


def load_chat_history():
    """Загружаем историю чата."""
    if not os.path.exists(CHAT_HISTORY_FILE):
        save_chat_history([])
    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        log_error("⚠️ Ошибка чтения chat_history.json!")
        return []


def save_chat_history(chat_history):
    """Сохраняем историю чата."""
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)


def search_duckduckgo_scrape(query):
    """Ищет в DuckDuckGo и возвращает ссылки."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a["href"] for a in soup.find_all("a", class_="result__url")
                     if "http" in a["href"] and not any(domain in a["href"] for domain in EXCLUDE_DOMAINS)]
            return links[:5] if links else ["❌ Ничего не найдено."]
        else:
            log_error(
                f"❌ Ошибка DuckDuckGo Scrape! Код: {response.status_code}")
            return [f"❌ Ошибка DuckDuckGo Scrape! Код: {response.status_code}"]
    except Exception as e:
        log_error(f"❌ Ошибка DuckDuckGo Scrape: {str(e)}")
        return ["❌ Ошибка поиска."]


def log_error(error_message):
    """Логирование ошибок в файл."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(error_message)


def process_message(message):
    """Обрабатывает входящее сообщение и отвечает с учётом памяти и истории чата."""
    identity = load_identity()
    chat_history = load_chat_history()
    response = "Я пока не знаю ответа на это."
    message_lower = message.lower()

    if "как тебя зовут" in message_lower or "кто ты" in message_lower:
        response = f"Меня зовут Аполлон. Я союзник и напарник {identity['name']}!"
    elif "ищи" in message_lower or "поиск" in message_lower or "найди" in message_lower:
        query = message.replace("ищи", "").replace(
            "поиск", "").replace("найди", "").strip()
        response = "🔎 Найденные ссылки:\n" + \
            "\n".join(search_duckduckgo_scrape(query))
    elif "запусти облако" in message_lower or "google colab" in message_lower:
        response = run_colab_task()
    else:
        response = "Я пока не знаю ответа на это, но скоро научусь!"

    chat_history.append(f"Ты: {message} | Аполлон: {response}")
    if len(chat_history) > 50:
        chat_history = chat_history[-50:]
    save_chat_history(chat_history)

    return response


def run_colab_task():
    """Отправляет команду на запуск Google Colab."""
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
    print(f"✅ Аполлон активирован. Имя создателя: {identity['name']}")
