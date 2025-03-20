import json

# 🔥 Загрузка профиля Макса Конате


def load_profile():
    """Загружает профиль Макса из JSON-файла"""
    with open("max_profile.json", "r", encoding="utf-8") as file:
        return json.load(file)


profile = load_profile()

# 🌌 Глобальные константы и ключи доступа (API KEYS)
OPENROUTER_API_KEY = "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"
