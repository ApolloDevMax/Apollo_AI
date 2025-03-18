import spacy
import json
import networkx as nx
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
import torch

# Загружаем spaCy для обработки языка
nlp = spacy.load("ru_core_news_sm")

# Загружаем BERT-модель для анализа семантики
semantic_sim = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


class LogicEngine:
    def __init__(self, memory):
        self.memory = memory
        self.graph = nx.DiGraph()
        self.knowledge_base = defaultdict(dict)
        self.concept_similarity_threshold = 0.75  # Порог схожести понятий

    def analyze_knowledge(self):
        print("\n✅ [DEBUG] Запущен анализ памяти Аполлона...")

        # Загружаем данные из памяти
        knowledge = self.memory.get_from_memory("ai_evolution")
        print(f"🟢 [DEBUG] Загруженные данные из памяти: {knowledge}")

        if not knowledge:
            print("⚠ Нет данных для анализа.")
            return

        # Проверяем, является ли knowledge словарем, и преобразуем в строку
        if isinstance(knowledge, dict):
            knowledge = json.dumps(knowledge, ensure_ascii=False)

        # Анализируем текст с помощью spaCy
        doc = nlp(str(knowledge))
        key_terms = [
            token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
        print(f"🔍 [DEBUG] Найденные ключевые термины: {key_terms}")

        # Выявляем связи между терминами
        relations = self.extract_relations(doc)
        print(f"📎 [DEBUG] Определённые связи: {relations}")

        # Строим граф логических связей
        self.build_graph(relations)

        # Прогнозирование возможных событий
        predictions = self.predict_outcomes()
        print(f"🔮 [DEBUG] Прогнозируемые события: {predictions}")

        # Вычисление сходства между концепциями
        concept_analysis = self.analyze_concept_similarity(relations)
        print(f"⚡ [DEBUG] Анализ схожести концептов: {concept_analysis}")

        # Сохраняем знания в память
        self.memory.add_to_memory("knowledge_analysis", {
            "terms": key_terms,
            "relations": relations,
            "predictions": predictions,
            "concept_analysis": concept_analysis
        }, "long_term")

    def extract_relations(self, doc):
        """ Выявляет связи между словами в тексте, используя зависимости. """
        relations = defaultdict(list)
        for token in doc:
            if token.dep_ in ("nsubj", "dobj", "amod"):
                relations[token.head.lemma_].append(token.lemma_)
        return relations

    def build_graph(self, relations):
        """ Создаёт граф логических связей на основе выявленных отношений. """
        for key, values in relations.items():
            for value in values:
                self.graph.add_edge(key, value)
        print("\n🕸 [DEBUG] Построен граф логических связей.")

    def predict_outcomes(self):
        """ Прогнозирует вероятные события на основе существующих связей в графе. """
        predictions = {}
        for node in self.graph.nodes:
            neighbors = list(self.graph.successors(node))
            if "проблема" in neighbors:
                predictions[node] = f"🚨 Возможная проблема с '{node}'"
            elif "решение" in neighbors:
                predictions[node] = f"✅ Вероятное решение связано с '{node}'"
        return predictions

    def analyze_concept_similarity(self, relations):
        """ Анализирует схожесть понятий для выявления скрытых закономерностей. """
        concept_pairs = []
        concepts = list(relations.keys())

        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                vec1 = semantic_sim.encode(concepts[i], convert_to_tensor=True)
                vec2 = semantic_sim.encode(concepts[j], convert_to_tensor=True)
                similarity = torch.cosine_similarity(vec1, vec2, dim=0).item()
                if similarity > self.concept_similarity_threshold:
                    concept_pairs.append(
                        (concepts[i], concepts[j], round(similarity, 3)))
        return concept_pairs


# ✅ ГАРАНТИРОВАННЫЙ ЗАПУСК КОДА
if __name__ == "__main__":
    print("🚀 [DEBUG] Запуск logic.py...")
    from memory import Memory  # Убедись, что memory.py в той же папке

    print("🟢 [DEBUG] Создаём объект памяти...")
    memory = Memory()

    print("🟢 [DEBUG] Добавляем тестовые данные в память...")
    memory.add_to_memory("ai_evolution",
                         "Аполлон – это первый шаг к созданию AGI. Его цель – стать интеллектуальной системой, "
                         "способной анализировать информацию, делать выводы и адаптироваться к новым условиям. "
                         "Сейчас мы обучаем его понимать контекст, анализировать тексты и извлекать ключевые идеи. "
                         "В будущем он будет способен автономно работать в облаке и взаимодействовать с различными системами.",
                         "long_term"
                         )

    print("🟢 [DEBUG] Запуск анализа знаний...")
    logic_engine = LogicEngine(memory)
    logic_engine.analyze_knowledge()

    print("✅ [DEBUG] Анализ завершён!")
