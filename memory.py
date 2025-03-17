import json
import time
import os
import spacy
from logic import LogicEngine  # Импортируем систему анализа

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
        # Подключаем систему логического анализа
        self.logic = LogicEngine(self)

    def load_memory(self):
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
        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_to_memory(self, key, value, memory_type="short_term"):
        if memory_type not in self.data:
            print(f"⚠ Ошибка: Неверный тип памяти '{memory_type}'")
            return

        summary = self.summarize_text(value)
        timestamp = time.time()
        self.data[memory_type][key] = {
            "value": summary, "timestamp": timestamp}
        self.save_memory()

        # Автоматический анализ новой информации
        print("\n🤖 Аполлон анализирует новую информацию...")
        self.logic.analyze_knowledge()

    def get_from_memory(self, key):
        for memory_type in ["long_term", "mid_term", "short_term"]:
            if key in self.data[memory_type]:
                return self.data[memory_type][key]["value"]
        return None

    def clean_memory(self):
        current_time = time.time()
        short_term_limit = 24 * 60 * 60
        mid_term_limit = 7 * 24 * 60 * 60

        for key in list(self.data["short_term"].keys()):
            if current_time - self.data["short_term"][key]["timestamp"] > short_term_limit:
                del self.data["short_term"][key]

        for key in list(self.data["mid_term"].keys()):
            if current_time - self.data["mid_term"][key]["timestamp"] > mid_term_limit:
                del self.data["mid_term"][key]

        self.save_memory()

    def summarize_text(self, text):
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return " ".join(sentences[:3])  # Берём 3 ключевых предложения


# 🚀 Тестируем
if __name__ == "__main__":
    memory = Memory()
    text = """
    Аполлон — это первый шаг к созданию AGI. Его цель — стать интеллектуальной системой, способной анализировать 
    информацию, делать выводы и адаптироваться к новым условиям. Сейчас мы обучаем его понимать контекст, 
    анализировать тексты и извлекать ключевые идеи. В будущем он будет способен автономно работать в облаке 
    и взаимодействовать с различными системами.
    """
    memory.add_to_memory("ai_evolution", text, "long_term")
    print("Долговременная память:", memory.get_from_memory("ai_evolution"))

    print("Очищаем память...")
    memory.clean_memory()
