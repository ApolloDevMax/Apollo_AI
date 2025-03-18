import json
import os
import statistics

DECISION_LOG = "decision_log.txt"
SELF_ANALYSIS_LOG = "self_analysis_log.txt"
ERROR_TRENDS_FILE = "error_trends.json"


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


def analyze_decisions(decisions):
    """Анализирует прошлые решения и выявляет ошибки"""
    total = len(decisions)
    if total == 0:
        return {"message": "Нет данных для анализа."}

    correct = sum(1 for d in decisions if d.get("result") == "correct")
    incorrect = total - correct
    error_rate = round((incorrect / total) * 100, 2)

    # Анализ типов ошибок
    error_types = {}
    for d in decisions:
        if d.get("result") == "incorrect":
            reason = d.get("error_reason", "unknown")
            error_types[reason] = error_types.get(reason, 0) + 1

    # Анализ трендов ошибок
    error_trend = analyze_error_trends(error_types)

    # Предсказание возможных проблем
    predictions = predict_future_issues(error_types)

    insights = {
        "total_decisions": total,
        "correct_decisions": correct,
        "incorrect_decisions": incorrect,
        "error_rate": error_rate,
        "error_types": error_types,
        "error_trend": error_trend,
        "predictions": predictions
    }

    return insights


def analyze_error_trends(error_types):
    """Анализирует динамику ошибок во времени"""
    if not os.path.exists(ERROR_TRENDS_FILE):
        save_json(ERROR_TRENDS_FILE, {})

    past_trends = load_json(ERROR_TRENDS_FILE, {})

    for error, count in error_types.items():
        past_trends[error] = past_trends.get(
            error, [])[-9:]  # Оставляем последние 10 записей
        past_trends[error].append(count)

    # Сохраняем обновленные тренды
    save_json(ERROR_TRENDS_FILE, past_trends)

    # Анализ динамики
    trends_analysis = {}
    for error, counts in past_trends.items():
        if len(counts) > 1:
            # Разница между последними двумя периодами
            diff = counts[-1] - counts[-2]
            if diff > 0:
                trend = f"⬆ Увеличение ({diff} новых случаев)"
            elif diff < 0:
                trend = f"⬇ Снижение ({abs(diff)} случаев меньше)"
            else:
                trend = "➖ Стабильно"
        else:
            trend = "🔄 Недостаточно данных"
        trends_analysis[error] = trend

    return trends_analysis


def predict_future_issues(error_types):
    """Делает предсказания на основе частых ошибок"""
    predictions = []
    for error, count in error_types.items():
        if count > 5:  # Если ошибка появляется часто
            predictions.append(f"⚠ Возможный рост ошибки '{error}' в будущем.")
    return predictions


def log_self_analysis(insights):
    """Записывает выводы самоанализа"""
    with open(SELF_ANALYSIS_LOG, "a", encoding="utf-8") as file:
        file.write(json.dumps(insights, ensure_ascii=False) + "\n")


def save_json(filename, data):
    """Сохраняет JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename, default_value):
    """Загружает JSON, если файл есть"""
    if not os.path.exists(filename):
        return default_value
    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default_value


def run_self_analysis():
    """Запускает процесс анализа ошибок и улучшения логики"""
    decisions = read_decision_log()
    insights = analyze_decisions(decisions)
    log_self_analysis(insights)
    print("✅ Самоанализ завершён. Лог записан в self_analysis_log.txt")


if __name__ == "__main__":
    run_self_analysis()
