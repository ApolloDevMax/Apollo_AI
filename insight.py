import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """Загружаем данные из памяти."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_insights():
    """Анализ данных и выявление закономерностей."""
    memory = load_memory()

    print("\n🔍 АНАЛИЗ ДАННЫХ:")

    if "INSIGHTS" not in memory:
        print("⚠️ Нет данных для анализа.")
        return

    insights = memory["INSIGHTS"]
    unique_insights = set(insights)

    print(f"\n📂 Всего инсайтов: {len(insights)}")
    print(f"🧠 Уникальных инсайтов: {len(unique_insights)}")
    print(f"🔄 Повторений: {len(insights) - len(unique_insights)}")

    if len(unique_insights) > 5:
        print("⚠️ Слишком много инсайтов, нужно систематизировать.")

    print("\n✅ Анализ завершён.")


if __name__ == "__main__":
    analyze_insights()
