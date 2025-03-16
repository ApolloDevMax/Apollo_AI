import json

MEMORY_FILE = "memory.json"


def fix_memory():
    """Исправляет кодировку файла памяти, удаляя \u041e и сохраняя текст в нормальном виде."""
    try:
        # Загружаем текущие данные
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Пересохраняем в правильной кодировке
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ Файл memory.json исправлен!")

    except Exception as e:
        print(f"❌ Ошибка при исправлении memory.json: {e}")


if __name__ == "__main__":
    fix_memory()
