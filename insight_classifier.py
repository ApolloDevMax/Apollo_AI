import json

MEMORY_FILE = "memory.json"
CLASSIFIED_INSIGHTS_FILE = "classified_insights.json"

CATEGORIES = {
    "финансы": ["заработок", "деньги", "инвестиции", "экономика", "доход"],
    "технологии": ["технологии", "Web3", "блокчейн", "стартап", "инновации"],
    "ИИ": ["искусственный интеллект", "нейросети", "машинное обучение", "AI"],
    "бизнес": ["автоматизация", "бизнес", "рынок", "предпринимательство"]
}


def load_memory():
    """Загружаем данные из памяти."""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_classified_insights(data):
    """Сохраняем классифицированные инсайты."""
    with open(CLASSIFIED_INSIGHTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def classify_insights():
    """Классифицируем инсайты по категориям."""
    memory = load_memory()
    classified_insights = {category: [] for category in CATEGORIES.keys()}

    for insight in memory.get("INSIGHTS", []):
        added = False
        for category, keywords in CATEGORIES.items():
            if any(keyword in insight.lower() for keyword in keywords):
                classified_insights[category].append(insight)
                added = True
                break
        if not added:
            classified_insights.setdefault("другое", []).append(insight)

    save_classified_insights(classified_insights)

    print("\n📂 Классификация инсайтов завершена.")
    for category, insights in classified_insights.items():
        print(f"🔹 {category.capitalize()}: {len(insights)} инсайтов")


if __name__ == "__main__":
    classify_insights()
