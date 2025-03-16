import json
import time
import random
from datetime import datetime

# Файлы
NEW_QUERIES_FILE = "new_queries.json"
MEMORY_FILE = "memory.json"
ERROR_LOG = "error_log.txt"


def load_queries():
    """Загружает новые запросы для изучения."""
    try:
        with open(NEW_QUERIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_memory(topic, data):
    """Сохраняет изученную информацию в память."""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = {}

    if topic not in memory:
        memory[topic] = []

    memory[topic].append(data)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)


def log_error(error):
    """Логирует ошибки в файл."""
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Ошибка: {error}\n")


def self_learning_loop():
    """Цикл самообучения."""
    while True:
        queries = load_queries()
        if not queries:
            print("⚠️ Нет новых запросов для изучения.")
            time.sleep(60)  # Ждем минуту перед новой проверкой
            continue

        for query in queries:
            print(f"🔍 Изучаем: {query}...")

            # Имитация сбора данных (в будущем заменим на реальный парсер или API)
            try:
                study_data = f"Глубокий анализ темы: {query} (эмуляция)"
                save_memory(query, study_data)
                print(f"✅ Данные сохранены в память для темы: {query}\n")
            except Exception as e:
                log_error(str(e))
                print(f"❌ Ошибка при обработке: {query}. Лог записан.")

        print("🔄 Завершен цикл самообучения. Ожидание перед следующим запуском...\n")
        time.sleep(600)  # Ожидание 10 минут перед следующим циклом


if __name__ == "__main__":
    self_learning_loop()
