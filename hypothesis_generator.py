import json

MEMORY_FILE = "memory.json"
HYPOTHESIS_FILE = "new_hypotheses.json"


def load_memory():
    """Загружаем данные памяти."""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_hypotheses(hypotheses):
    """Сохраняем новые гипотезы."""
    with open(HYPOTHESIS_FILE, "w", encoding="utf-8") as f:
        json.dump(hypotheses, f, indent=4, ensure_ascii=False)


def generate_hypotheses():
    """Генерируем новые гипотезы на основе инсайтов."""
    memory_data = load_memory()
    insights = memory_data.get("INSIGHTS", [])

    new_hypotheses = []

    for insight in insights:
        # Простейший алгоритм: создаём гипотезу на основе инсайта
        hypothesis = f"Что если {insight.lower()}?"
        new_hypotheses.append(hypothesis)

    if new_hypotheses:
        save_hypotheses(new_hypotheses)
        print("\n🧠 **Аполлон сформировал новые гипотезы:**")
        for hyp in new_hypotheses:
            print(f"🔹 {hyp}")
    else:
        print("\n⚠️ **Нет новых гипотез для формирования.**")


if __name__ == "__main__":
    generate_hypotheses()
