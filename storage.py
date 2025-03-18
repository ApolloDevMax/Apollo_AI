import json
import os
import time


class NewsStorage:
    def __init__(self, storage_file="news_storage.json"):
        self.storage_file = storage_file
        self.data = self.load_storage()

    def load_storage(self):
        """ Загружает существующую базу новостей или создаёт новую. """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("⚠ Ошибка в файле хранения, создаём новый...")
        return {"news": []}

    def save_storage(self):
        """ Сохраняет обновлённую базу новостей. """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_news(self, title, source, url, timestamp=None):
        """ Добавляет новую новость в базу, если её ещё нет. """
        if not timestamp:
            timestamp = time.time()

        # Проверяем, есть ли уже такая новость
        for news in self.data["news"]:
            if news["title"] == title:
                print(f"🔍 Новость уже в базе: {title}")
                return False

        # Добавляем новость
        self.data["news"].append({
            "title": title,
            "source": source,
            "url": url,
            "timestamp": timestamp
        })
        self.save_storage()
        print(f"✅ Новость добавлена: {title}")
        return True

    def get_recent_news(self, limit=5):
        """ Возвращает последние N новостей. """
        return sorted(self.data["news"], key=lambda x: x["timestamp"], reverse=True)[:limit]


# 🚀 Тестируем модуль хранения новостей
if __name__ == "__main__":
    storage = NewsStorage()
    storage.add_news("Тестовая новость", "GNews", "https://gnews.io/test")
    print("\n📌 Последние новости:")
    for news in storage.get_recent_news():
        print(f"📰 {news['title']} – {news['source']} ({news['url']})")
