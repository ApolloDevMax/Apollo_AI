# memory.py
import json
import os

MEMORY_FILE = "memory.json"

# Загрузка памяти


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Функция сохранения памяти


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Добавление информации в память


def add_to_memory(category, content):
    memory = load_memory()
    if category not in memory:
        memory[category] = []
    if content not in memory[category]:
        memory[category].append(content)
        save_memory(memory)
        print(f"✅ Добавлено в '{category}': {content}")
    else:
        print(f"⚠️ Уже существует в '{category}'")

# Чтение памяти


def read_memory(category=None):
    memory = load_memory()
    return memory.get(category, []) if category else memory
