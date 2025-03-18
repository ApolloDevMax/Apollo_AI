import json
import os

DECISION_LOG = "decision_log.txt"
NEW_HYPOTHESES_FILE = "new_hypotheses.json"
ERROR_RECOVERY_LOG = "error_recovery_log.txt"


def read_decision_log():
    """Считывает логи решений Аполлона"""
    if not os.path.exists(DECISION_LOG):
        return []

    with open(DECISION_LOG, "r", encoding="utf-8") as file:
        lines = file.readlines()

    decisions = []
    for line in lines:
        try:
            decision = json.loads(line.strip())
            decisions.append(decision)
        except json.JSONDecodeError:
            continue  # Пропускаем битые строки
    return decisions


def find_errors(decisions):
    """Находит ошибки в принятых решениях"""
    errors = [d for d in decisions if d.get("result") == "incorrect"]
    return errors


def rollback_errors(errors):
    """Генерирует новые исправленные гипотезы вместо ошибочных решений"""
    corrections = []
    for error in errors:
        corrections.append({
            "hypothesis": f"Исправление ошибки: {error.get('error_reason', 'unknown')}",
            "correction_strategy": "Отменить предыдущее решение и пересчитать",
            "status": "pending"
        })

    return corrections


def save_corrections(corrections):
    """Сохраняет исправленные гипотезы в файл"""
    if not corrections:
        print("❌ Нет ошибок для отката.")
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

    # Логируем исправления
    with open(ERROR_RECOVERY_LOG, "a", encoding="utf-8") as file:
        file.write(json.dumps(corrections, ensure_ascii=False) + "\n")

    print(f"✅ Ошибки откатаны. Исправления сохранены в {NEW_HYPOTHESES_FILE}")


def run_error_recovery():
    """Запускает процесс отката ошибок"""
    decisions = read_decision_log()
    errors = find_errors(decisions)
    corrections = rollback_errors(errors)
    save_corrections(corrections)


if __name__ == "__main__":
    run_error_recovery()
