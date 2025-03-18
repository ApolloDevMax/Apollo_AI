import json
import os

SELF_ANALYSIS_LOG = "self_analysis_log.txt"
NEW_HYPOTHESES_FILE = "new_hypotheses.json"


def read_last_analysis():
    """Считывает последний отчёт самоанализа"""
    if not os.path.exists(SELF_ANALYSIS_LOG):
        return None

    with open(SELF_ANALYSIS_LOG, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        return None

    return json.loads(lines[-1].strip())  # Берём последний анализ


def generate_corrections(insights):
    """Генерирует исправления на основе анализа ошибок"""
    if not insights or "error_types" not in insights:
        return []

    corrections = []
    for error, count in insights["error_types"].items():
        corrections.append({
            "hypothesis": f"Исправление ошибки: {error}",
            "correction_strategy": "Перепроверить данные и изменить логику",
            "status": "pending"
        })

    return corrections


def save_corrections(corrections):
    """Сохраняет новые гипотезы для исправления в файл"""
    if not corrections:
        print("❌ Нет исправлений для сохранения.")
        return

    if os.path.exists(NEW_HYPOTHESES_FILE):
        with open(NEW_HYPOTHESES_FILE, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(corrections)

    with open(NEW_HYPOTHESES_FILE, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    print(f"✅ Исправления сохранены в {NEW_HYPOTHESES_FILE}")


def run_self_correction():
    """Запускает процесс исправления ошибок"""
    insights = read_last_analysis()
    corrections = generate_corrections(insights)
    save_corrections(corrections)


if __name__ == "__main__":
    run_self_correction()
