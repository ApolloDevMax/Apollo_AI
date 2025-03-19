import requests
import json
import time
import random
import logging
from collections import Counter
import nltk
from nltk.corpus import stopwords
from urllib.parse import quote

# === 🔥 Настройки API ===
GOOGLE_API_KEY = "AIzaSyC3osOG8zTc7WLbyNYAQTTAvuRLb2tiS8E"
GOOGLE_CX_KEY = "2518e0c19fbe043a0"

# === 🔥 Логирование ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# === 🔥 Загружаем базу знаний ===
try:
    with open("knowledge_base.json", "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    knowledge_base = []

# === 🔥 Загружаем список исследованных тем ===
try:
    with open("explored_topics.json", "r", encoding="utf-8") as f:
        explored_topics = json.load(f)
except FileNotFoundError:
    explored_topics = []

# === 🔥 Загрузка NLTK ===
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("russian")) | set(stopwords.words("english"))

# === 🔥 Чёрный список тем (чтобы не брать мусор) ===
BLACKLIST_TOPICS = {"jan", "inc.", "изменение", "google", "error",
                    "info", "finance", "company", "university", "professor", "pixel"}


def google_search(query):
    """Ищет информацию в Google и возвращает уникальные результаты"""
    url = f"https://www.googleapis.com/customsearch/v1?q={quote(query)}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [item["snippet"] for item in data.get("items", [])]
        else:
            return [f"❌ Ошибка запроса: {response.status_code}"]
    except Exception as e:
        return [f"❌ Ошибка: {str(e)}"]


def clean_text(text):
    """Удаляет стоп-слова и лишние символы"""
    words = text.lower().split()
    return [word for word in words if word not in STOPWORDS and len(word) > 2]


def filter_results(results):
    """Фильтрует ненужные результаты"""
    filtered = []
    for res in results:
        if len(res) < 30:  # Слишком короткие фразы пропускаем
            continue
        # Если начинается с троеточия, пропускаем (обрезанный текст)
        if "..." in res[:10]:
            continue
        filtered.append(res)
    return filtered


def analyze_knowledge():
    """Анализирует знания и делает выводы"""
    if len(knowledge_base) < 10:
        return "Мало данных для анализа."

    word_count = Counter()
    for item in knowledge_base:
        word_count.update(clean_text(item))

    top_terms = [term for term, count in word_count.most_common(5)
                 if term not in BLACKLIST_TOPICS and term != "..."]

    return f"📊 Выводы Аполлона:\n🔹 ТОП-5 ключевых слов: {top_terms}"


def find_new_topic():
    """Генерирует новую тему на основе уже изученных данных"""
    if not knowledge_base:
        return random.choice(["AGI", "Квантовые вычисления", "Будущее AI", "Web3", "Макс Конате"])

    # **Ищем повторяющиеся термины** – они могут быть интересны!
    word_count = Counter()
    for item in knowledge_base:
        word_count.update(clean_text(item))

    common_terms = [term for term, count in word_count.most_common(20)
                    if term not in explored_topics and term not in BLACKLIST_TOPICS and len(term) > 3]

    if common_terms:
        new_topic = random.choice(common_terms)
        explored_topics.append(new_topic)
        return new_topic
    else:
        return random.choice(["AGI", "Web3", "Будущее AI", "Макс Конате", "Инновации в спорте"])


def should_dive_deeper(query):
    """Решает, стоит ли углубляться в тему"""
    results = google_search(query)
    relevant_results = [res for res in filter_results(
        results) if len(res.split()) > 10]

    if len(relevant_results) > 2:
        logging.info(f"🔬 Аполлон нашел много инфы про {query} – углубляемся!")
        return True
    return False


def self_learning():
    """🔥 Бесконечное саморазвитие Аполлона 🔥"""
    global knowledge_base, explored_topics
    iteration = 0

    try:
        while True:
            query = find_new_topic()
            logging.info(f"🔍 Аполлон изучает: {query}")

            # **Делаем запрос**
            results = google_search(query)

            # **Фильтруем дубликаты и мусор**
            unique_results = [res for res in filter_results(
                results) if res not in knowledge_base]

            if unique_results:
                knowledge_base.extend(unique_results)
                # Показываем 3 первых
                logging.info(f"📚 Новые знания: {unique_results[:3]}")

            # **Сохраняем базу знаний**
            with open("knowledge_base.json", "w", encoding="utf-8") as f:
                json.dump(knowledge_base, f, indent=4, ensure_ascii=False)
                logging.info("💾 База знаний обновлена!")

            # **Сохраняем список исследованных тем**
            with open("explored_topics.json", "w", encoding="utf-8") as f:
                json.dump(explored_topics, f, indent=4, ensure_ascii=False)

            # **Анализируем знания**
            analysis = analyze_knowledge()
            logging.info(analysis)

            # **Если тема реально интересная – продолжаем её изучать**
            if should_dive_deeper(query):
                logging.info(f"🔎 Продолжаем углубляться в {query}!")
                explored_topics.append(query)  # Добавляем в список изученных

            iteration += 1
            time.sleep(60)  # Ждём 1 минуту перед следующим поиском

    except KeyboardInterrupt:
        logging.info("⏹️  Аполлон остановлен. Прогресс сохранён. 🚀")


# === 🔥 Запуск ===
if __name__ == "__main__":
    self_learning()
