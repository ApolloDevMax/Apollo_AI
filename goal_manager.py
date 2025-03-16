import json
import os

GOALS_FILE = "goals.json"
MEMORY_FILE = "memory.json"


def load_goals():
    """Загружаем текущие цели Аполлона."""
    if not os.path.exists(GOALS_FILE):
        return {"active": [], "completed": []}
    with open(GOALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_goals(goals):
    """Сохраняем обновленные цели."""
    with open(GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(goals, f, indent=4, ensure_ascii=False)


def load_memory():
    """Загружаем данные из памяти."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def update_goals():
    """Обновляем цели на основе прогресса Аполлона."""
    goals = load_goals()
    memory = load_memory()

    completed_goals = []
    new_goals = []

    print("\n🎯 Проверяем выполнение целей...\n")

    for goal in goals["active"]:
        if any(goal in insight for insight in memory.get("INSIGHTS", [])):
            print(f"🏆 Цель выполнена: {goal}")
            completed_goals.append(goal)
        else:
            new_goals.append(goal)

    goals["active"] = new_goals
    goals["completed"].extend(completed_goals)

    save_goals(goals)

    print("\n📌 Текущие цели:")
    for goal in goals["active"]:
        print(f"- {goal}")

    print("\n🏅 Выполненные цели:")
    for goal in completed_goals:
        print(f"✅ {goal}")


if __name__ == "__main__":
    update_goals()
