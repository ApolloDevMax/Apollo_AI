import json
import os
import time
from collections import deque

MEMORY_FILE = "memory.json"
TEMP_MEMORY_FILE = "temp_memory.json"


class MemoryManager:
    def __init__(self):
        self.memory = self.load_memory()
        # Краткосрочная память (быстро забывает)
        self.short_term = deque(maxlen=10)
        self.medium_term = []  # Среднесрочная память (несколько дней)
        # Долговременная память (навсегда)
        self.long_term = self.memory.get("long_term", {})

    def load_memory(self):
        """Загружает память из файла."""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"long_term": {}}

    def save_memory(self):
        """Сохраняет память в файл."""
        self.memory["long_term"] = self.long_term
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=4)

    def add_to_memory(self, category, data, importance=1):
        """Добавляет данные в память с приоритетами."""
        entry = {"text": data, "timestamp": time.time(),
                 "importance": importance}

        # Краткосрочная память (временные данные)
        self.short_term.append(entry)

        # Среднесрочная память (данные средней важности)
        if importance >= 3:
            self.medium_term.append(entry)

        # Долговременная память (ключевые данные)
        if importance >= 5:
            if category not in self.long_term:
                self.long_term[category] = []
            self.long_term[category].append(entry)

        self.save_memory()

    def analyze_memory(self):
        """Анализирует память, выявляет ценные паттерны."""
        print("\n📊 АНАЛИЗ ПАМЯТИ:")
        for category, entries in self.long_term.items():
            print(f"\n📂 Категория: {category} ({len(entries)} записей)")
            for entry in entries[-3:]:  # Показываем последние 3 записи
                print(f"🔹 {entry['text']} (Важность: {entry['importance']})")

    def clear_temp_memory(self):
        """Очищает краткосрочную память (ненужные временные данные)."""
        self.short_term.clear()
        self.medium_term = []
        print("🧹 Краткосрочная память очищена.")


if __name__ == "__main__":
    manager = MemoryManager()
    manager.analyze_memory()
