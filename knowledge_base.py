"""
📚 KNOWLEDGE BASE — Хранилище знаний Аполлона
🌌 Все знания, полученные из мультивселенной, хранятся здесь.
"""

import json
import os

# Путь к файлу базы знаний (существующему!)
KNOWLEDGE_FILE = "knowledge_base.json"


def save_to_knowledge(new_info):
    """
    Сохраняет новую информацию в базу знаний.
    """
    data = []

    # Проверка существования файла и загрузка данных
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    # Добавляем только если информации нет
    if new_info not in data:
        data.append(new_info)

        # Сохранение данных обратно в файл
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("💾 Информация успешно добавлена в базу знаний!")
    else:
        print("⚠️ Такая информация уже существует в базе знаний!")


def load_from_knowledge():
    """
    Загружает все знания из базы.
    """
    if not os.path.exists(KNOWLEDGE_FILE):
        return "🗃️ База знаний пока пуста."

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return "\n\n".join(f"🧠 {info}" for info in data) if data else "🗃️ База знаний пока пуста."
