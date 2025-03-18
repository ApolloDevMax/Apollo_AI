import json
import os
import random

NEW_HYPOTHESES_FILE = "new_hypotheses.json"
TESTED_HYPOTHESES_FILE = "tested_hypotheses.json"
TEST_LOG = "hypothesis_test_log.txt"


def read_hypotheses():
    """Считывает новые гипотезы для тестирования"""
    if not os.path.exists(NEW_HYPOTHESES_FILE):
        return []

    with open(NEW_HYPOTHESES_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data  # Всё в порядке
            elif isinstance(data, dict):
                # Если почему-то одиночный объект, оборачиваем в список
                return [data]
        except json.JSONDecodeError:
            return []

    return []


def test_hypothesis(hypothesis):
    """Простая логика тестирования гипотез (можно заменить на сложный алгоритм)"""
    if isinstance(hypothesis, str):
        try:
            # Пробуем преобразовать строку в JSON
            hypothesis = json.loads(hypothesis)
        except json.JSONDecodeError:
            return None  # Если не удалось – пропускаем

    if not isinstance(hypothesis, dict) or "hypothesis" not in hypothesis:
        return None  # Пропускаем некорректные данные

    # Имитация теста (в реальности тут может быть алгоритм машинного обучения)
    test_result = random.choice(["valid", "invalid"])

    return {
        "hypothesis": hypothesis["hypothesis"],
        "status": test_result,
        "correction_needed": test_result == "invalid"
    }


def process_hypotheses(hypotheses):
    """Тестирует и сортирует гипотезы"""
    valid_hypotheses = []
    invalid_hypotheses = []

    for h in hypotheses:
        result = test_hypothesis(h)
        if result:
            if result["status"] == "valid":
                valid_hypotheses.append(result)
            else:
                invalid_hypotheses.append(result)

    return valid_hypotheses, invalid_hypotheses


def save_test_results(valid_hypotheses, invalid_hypotheses):
    """Сохраняет результаты тестов"""
    all_tested = valid_hypotheses + invalid_hypotheses

    with open(TESTED_HYPOTHESES_FILE, "w", encoding="utf-8") as file:
        json.dump(all_tested, file, ensure_ascii=False, indent=4)

    with open(TEST_LOG, "a", encoding="utf-8") as file:
        file.write(json.dumps(all_tested, ensure_ascii=False) + "\n")

    print(
        f"✅ Гипотезы протестированы. Результаты сохранены в {TESTED_HYPOTHESES_FILE}")


def run_hypothesis_tester():
    """Запускает тестирование гипотез"""
    hypotheses = read_hypotheses()

    if not hypotheses:
        print("❌ Нет новых гипотез для тестирования.")
        return

    valid_hypotheses, invalid_hypotheses = process_hypotheses(hypotheses)
    save_test_results(valid_hypotheses, invalid_hypotheses)


if __name__ == "__main__":
    run_hypothesis_tester()
