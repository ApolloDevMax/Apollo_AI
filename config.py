import json


def load_profile():
    """Загружает профиль Макса из JSON-файла"""
    with open("max_profile.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


profile = load_profile()

# Пример использования
print(f"🤖 Аполлон загружен. Имя владельца: {profile['identity']['name']}")
