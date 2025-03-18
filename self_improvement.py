import json
import os
import random
import subprocess
from collections import Counter

# Пути к файлам
MEMORY_FILE = "memory.json"
HYPOTHESES_FILE = "hypotheses.json"
ERROR_LOG = "error_log.txt"

# ==============================
# 🔥 ФУНКЦИИ РАБОТЫ С ПАМЯТЬЮ
# ==============================


def load_memory():
    """Загружает память Аполлона."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_error("❌ Ошибка чтения памяти: файл повреждён!")
        return {}


def analyze_memory():
    """Анализирует память, выявляет ключевые темы и формирует новые гипотезы."""
    memory = load_memory()
    keywords = []

    print("\n📊 АНАЛИЗ ПАМЯТИ:")

    if not memory:
        print("⚠️ Память пуста! Добавьте информацию для анализа.")
        return []

    new_queries = []
    for category, entries in memory.items():
        if not isinstance(entries, list):
            print(
                f"⚠️ Ошибка формата в категории '{category}'! Ожидался список, но получен {type(entries).__name__}. Пропускаю.")
            continue

        print(f"\n📂 Категория: {category}")
        clean_entries = [str(entry) for entry in entries if isinstance(
            entry, (str, int))]  # Избегаем словарей
        counter = Counter(clean_entries)

        for entry, count in counter.most_common(5):
            print(f"🔹 {entry} (Повторений: {count})")
            # Берём два первых слова из записи
            keywords.extend(entry.split()[:2])

    if not keywords:
        print("⚠️ Недостаточно данных для формирования новых гипотез.")
        return []

    # Генерируем новые гипотезы на основе частых тем
    new_queries = [
        f"Как улучшить {random.choice(keywords)}?" for _ in range(3)]

    print("\n🧠 Сформированы новые гипотезы:")
    for query in new_queries:
        print(f"💡 {query}")

    return new_queries


def save_hypotheses(hypotheses):
    """Сохраняет новые гипотезы в файл."""
    try:
        with open(HYPOTHESES_FILE, "w", encoding="utf-8") as f:
            json.dump(hypotheses, f, indent=4, ensure_ascii=False)
        print("\n✅ Гипотезы сохранены для тестирования.")
    except Exception as e:
        log_error(f"Ошибка сохранения гипотез: {e}")

# ==============================
# 🔥 САМООБРАЗОВАНИЕ АПОЛЛОНА
# ==============================


def self_learning():
    """Запускает процесс самообучения, анализирует гипотезы и улучшает код."""
    new_hypotheses = analyze_memory()
    if new_hypotheses:
        save_hypotheses(new_hypotheses)

    # Автоматический анализ гипотез
    try:
        print("\n🚀 Запускаю тестирование гипотез...")
        subprocess.run(["python", "hypothesis_tester.py"], check=True)
    except Exception as e:
        log_error(f"Ошибка запуска hypothesis_tester.py: {e}")

    # Автоматическое исправление ошибок
    try:
        print("\n🔧 Запускаю самоисправление кода...")
        subprocess.run(["python", "self_correction.py"], check=True)
    except Exception as e:
        log_error(f"Ошибка запуска self_correction.py: {e}")

# ==============================
# 🔥 ЛОГИРОВАНИЕ ОШИБОК
# ==============================


def log_error(error_message):
    """Логирует ошибки."""
    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(error_message + "\n")
    print(f"❌ Ошибка: {error_message} (записано в error_log.txt)")

# ==============================
# 🔥 ЗАПУСК САМОРАЗВИТИЯ
# ==============================


if __name__ == "__main__":
    try:
        print("\n🚀 **Аполлон начинает процесс саморазвития** 🚀")
        self_learning()
        print("\n✅ **Саморазвитие завершено успешно!**")
    except Exception as e:
        log_error(f"❌ Критическая ошибка саморазвития: {e}")
