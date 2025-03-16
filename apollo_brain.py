# apollo_brain.py
import memory
import analyzer
import self_learning
import decision_maker

print("\n🚀 Запуск Аполлона...\n")

# Загружаем память
knowledge = memory.load_memory()
print("🔍 Загружена память. Количество категорий:", len(knowledge))

# Запускаем анализ данных
analyzer.run_analysis()

# Запускаем систему самообучения
self_learning.run_self_learning()

# Запускаем принятие решений
decision_maker.make_decision()

print("\n✅ Аполлон завершил анализ, обучение и принятие решений!")
