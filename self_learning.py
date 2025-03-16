import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """Загружаем сохранённые данные."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):
    """Сохраняем обновлённую память."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def analyze_and_learn():
    """Аполлон анализирует данные и делает выводы."""
    memory_data = load_memory()

    if not memory_data:
        print("🛑 Нет данных для анализа.")
        return

    insights = []

    for category, entries in memory_data.items():
        if category == "Internet_Search":
            for item in entries:
                query = item["query"]
                results = item["results"]
                # Берем первый результат как инсайт
                key_insight = results[0] if results else None

                if key_insight:
                    insight_text = f"🔍 Вывод по '{query}': {key_insight}"
                    insights.append(insight_text)

    if insights:
        memory_data.setdefault("INSIGHTS", []).extend(insights)
        save_memory(memory_data)

        print("\n✅ Аполлон завершил анализ и самообучение!")
        for insight in insights:
            print(f"⚡ {insight}")


if __name__ == "__main__":
    analyze_and_learn()
