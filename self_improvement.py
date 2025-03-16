import json
import os
import random
from collections import Counter

# Пути к файлам
MEMORY_FILE = "memory.json"
NEW_QUERIES_FILE = "new_queries.json"
ERROR_LOG = "error_log.txt"


def load_memory():
    """Загружает память Аполлона."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_memory():
    """Анализирует память, выявляет ключевые темы и формирует новые запросы."""
    memory = load_memory()
    keywords = []

    print("\n📊 АНАЛИЗ ПАМЯТИ:")

    if not memory:
        print("⚠️ Память пуста! Добавьте информацию для анализа.")
        return []

    for category, entries in memory.items():
        print(f"\n📂 Категория: {category}")
        counter = Counter(entries)
        # Берем топ-5 повторяющихся
        for entry, count in counter.most_common(5):
            print(f"🔹 {entry} (Повторений: {count})")
            keywords.extend(entry.split()[:2])  # Извлекаем 2 ключевых слова

    if not keywords:
        print("⚠️ Недостаточно данных для формирования новых вопросов.")
        return []

    # Формируем новые вопросы на основе частых тем
    new_queries = [" ".join(random.sample(keywords, 2)
                            ) + " AI" for _ in range(3)]

    print("\n🧠 Сформированы новые вопросы для изучения:")
    for query in new_queries:
        print(f"🔍 {query}")

    return new_queries


def save_new_queries(queries):
    """Сохраняет новые вопросы в файл."""
    try:
        with open(NEW_QUERIES_FILE, "w", encoding="utf-8") as f:
            json.dump(queries, f, indent=4, ensure_ascii=False)
        print("\n✅ Вопросы сохранены для дальнейшего изучения.")
    except Exception as e:
        log_error(f"Ошибка сохранения вопросов: {e}")


def log_error(error_message):
    """Логирует ошибки в error_log.txt."""
    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(f"❌ Ошибка: {error_message} (записано в error_log.txt)")


if __name__ == "__main__":
    try:
        new_queries = analyze_memory()
        if new_queries:
            save_new_queries(new_queries)
    except Exception as e:
        log_error(f"Ошибка выполнения self_improvement.py: {e}")
