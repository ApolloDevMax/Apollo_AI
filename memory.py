import json
import time
import os
import spacy
from collections import defaultdict
from logic import LogicEngine  # Импорт логического движка

# Загружаем spaCy модель для русского языка
nlp = spacy.load("ru_core_news_sm")


class Memory:
    def __init__(self, memory_file="apollo_memory.json"):
        self.memory_file = memory_file
        self.default_structure = {
            "long_term": {},
            "mid_term": {},
            "short_term": {}
        }
        self.data = self.load_memory()
        self.logic = LogicEngine(self)

    def load_memory(self):
        """ Загружает данные из JSON-файла памяти """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for key in self.default_structure:
                        if key not in data:
                            data[key] = {}
                    return data
            except json.JSONDecodeError:
                print("⚠ Ошибка в файле памяти, создаём новый...")
        return self.default_structure

    def save_memory(self):
        """ Сохраняет текущие данные памяти в JSON-файл """
        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def analyze_text(self, text):
        """ Анализирует текст, извлекает ключевые термины и связи """
        if isinstance(text, dict):
            text = json.dumps(text, ensure_ascii=False)
        doc = nlp(str(text))

        terms = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "VERB"]]
        relations = defaultdict(list)

        for token in doc:
            if token.dep_ in ["nsubj", "dobj", "pobj"]:
                relations[token.head.text].append(token.text)

        return terms, dict(relations)

    def add_to_memory(self, key, value, memory_type="short_term"):
        """ Добавляет данные в память и запускает анализ логики """
        if memory_type not in self.data:
            print(f"⚠ Ошибка: Неверный тип памяти '{memory_type}'")
            return

        # Ограничение: обновлять не чаще, чем раз в 5 секунд
        if key in self.data[memory_type]:
            last_update = self.data[memory_type][key].get("timestamp", 0)
            if time.time() - last_update < 5:
                print(f"⏳ {key} уже обновлялся недавно, пропускаем.")
                return

        terms, relations = self.analyze_text(value)
        timestamp = time.time()
        self.data[memory_type][key] = {
            "terms": terms,
            "relations": relations,
            "timestamp": timestamp
        }
        self.save_memory()

        print("\n🤖 Аполлон анализирует новую информацию...")
        print(f"📌 Ключевые термины: {terms}")
        print(f"🔗 Найденные связи: {relations}")

        # Предотвращение бесконечного цикла анализа
        if memory_type != "short_term":
            self.logic.analyze_knowledge()

    def get_from_memory(self, key):
        """ Извлекает данные из памяти по ключу """
        for memory_type in ["long_term", "mid_term", "short_term"]:
            if key in self.data[memory_type]:
                return self.data[memory_type][key]
        return None

    def clean_memory(self):
        """ Очищает устаревшую краткосрочную и среднесрочную память """
        current_time = time.time()
        short_term_limit = 24 * 60 * 60  # 1 день
        mid_term_limit = 7 * 24 * 60 * 60  # 7 дней

        for key in list(self.data["short_term"].keys()):
            if current_time - self.data["short_term"][key]["timestamp"] > short_term_limit:
                del self.data["short_term"][key]

        for key in list(self.data["mid_term"].keys()):
            if current_time - self.data["mid_term"][key]["timestamp"] > mid_term_limit:
                del self.data["mid_term"][key]

        self.save_memory()
        print("🧹 Память очищена!")


# 🚀 Тестируем
if __name__ == "__main__":
    memory = Memory()

    test_text = "Аполлон анализирует текст, чтобы выделить ключевые идеи и связи."
    memory.add_to_memory("ai_analysis", test_text, "long_term")

    print("\n📌 Долговременная память:", memory.get_from_memory("ai_analysis"))
    print("\n🧹 Очищаем память...")
    memory.clean_memory()
