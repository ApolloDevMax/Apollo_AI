import spacy

nlp = spacy.load("ru_core_news_sm")


class LogicEngine:
    def __init__(self, memory):
        self.memory = memory

    def analyze_knowledge(self):
        """ Анализирует знания Аполлона и делает выводы. """
        print("\n🤖 Анализ памяти Аполлона...")
        knowledge = self.memory.get_from_memory("ai_evolution")
        if not knowledge:
            print("❌ Нет данных для анализа!")
            return

        doc = nlp(knowledge)
        # Извлекаем ключевые сущности
        entities = [ent.text for ent in doc.ents]
        print(
            f"📌 Ключевые идеи: {', '.join(entities) if entities else 'Нет найденных ключевых идей'}")

        # Простейший вывод
        if "AGI" in knowledge:
            print("🚀 Вывод: Аполлон стремится к сильному ИИ.")
        else:
            print("⚡ Вывод: Нет информации о целях AGI.")

        return entities


# Тест
if __name__ == "__main__":
    from memory import Memory

    memory = Memory()
    logic = LogicEngine(memory)
    logic.analyze_knowledge()
