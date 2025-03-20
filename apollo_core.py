import json
import random
import logging
import threading
from openrouter_api import wikipedia_search, ask_openrouter

# 🔥 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# ⚡ Флаг для управления обучением
stop_event = threading.Event()

# ⚡️ Загружаем профиль Макса
with open("max_profile.json", "r", encoding="utf-8") as file:
    max_profile = json.load(file)

# 🌌 Активация Аполлона


def quantum_connection():
    logging.info("⚡ Аполлон активирован. Готов к квантовому взаимодействию!")

# 🔍 Выбираем тему для изучения


def select_topic():
    topics = ["AGI", "Квантовый интеллект", "Web3",
              "Финансовый рынок", "Илон Маск", "Искусственный интеллект"]
    return random.choice(topics)

# 📖 Аполлон изучает тему и анализирует данные


def learn_new_topic(topic):
    logging.info(f"🔍 Аполлон изучает тему: {topic}")

    wiki_results = wikipedia_search(topic)

    if wiki_results and len(wiki_results) > 0:
        logging.info(f"📖 Wikipedia: {wiki_results}")

        # Выбираем первую найденную статью
        first_article = wiki_results[0]
        logging.info(f"📖 Аполлон читает статью: {first_article}")

        # Отправляем статью в ИИ для анализа
        ai_analysis = ask_openrouter(
            f"Анализируй статью из Wikipedia о {topic} и сделай выводы.")
        logging.info(f"🤖 Аполлон анализирует: {ai_analysis}")

    else:
        logging.warning("❌ Wikipedia не нашла ничего полезного.")


# 🚀 Запуск
if __name__ == "__main__":
    quantum_connection()
    topic = select_topic()
    learn_new_topic(topic)
