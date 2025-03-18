import json
import os
import matplotlib.pyplot as plt

SELF_ANALYSIS_LOG = "self_analysis_log.txt"
TEST_LOG = "hypothesis_test_log.txt"


def read_analysis_data():
    """Считывает логи самоанализа и корректирует формат данных"""
    if not os.path.exists(SELF_ANALYSIS_LOG):
        return []

    with open(SELF_ANALYSIS_LOG, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        try:
            parsed_line = json.loads(line.strip())
            if isinstance(parsed_line, str):  # Если по какой-то причине это строка
                parsed_line = json.loads(parsed_line)
            data.append(parsed_line)
        except json.JSONDecodeError:
            continue
    return data


def read_test_data():
    """Считывает логи тестирования гипотез"""
    if not os.path.exists(TEST_LOG):
        return []

    with open(TEST_LOG, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        try:
            parsed_line = json.loads(line.strip())
            if isinstance(parsed_line, str):
                parsed_line = json.loads(parsed_line)
            data.append(parsed_line)
        except json.JSONDecodeError:
            continue
    return data


def plot_progress():
    """Строит графики эволюции Аполлона"""
    analysis_data = read_analysis_data()
    test_data = read_test_data()

    if not analysis_data:
        print("❌ Нет данных для анализа.")
        return

    # Данные для анализа ошибок
    iterations = list(range(1, len(analysis_data) + 1))
    error_rates = [entry.get("error_rate", 0) for entry in analysis_data]
    correct_decisions = [entry.get("correct_decisions", 0)
                         for entry in analysis_data]

    # График ошибок
    plt.figure(figsize=(12, 5))
    plt.plot(iterations, error_rates, marker="o",
             linestyle="-", label="Ошибка (%)")
    plt.xlabel("Итерации")
    plt.ylabel("Доля ошибок")
    plt.title("Прогресс Аполлона: Ошибки со временем")
    plt.legend()
    plt.grid(True)
    plt.show()

    # График успешных решений
    plt.figure(figsize=(12, 5))
    plt.plot(iterations, correct_decisions, marker="s",
             linestyle="-", color="g", label="Корректные решения")
    plt.xlabel("Итерации")
    plt.ylabel("Количество верных решений")
    plt.title("Прогресс Аполлона: Корректные гипотезы")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Анализ тестов гипотез
    valid_tests = sum(1 for test in test_data if isinstance(
        test, list) and test and test[0].get("status") == "valid")
    invalid_tests = sum(1 for test in test_data if isinstance(
        test, list) and test and test[0].get("status") == "invalid")

    labels = ["Успешные гипотезы", "Ошибочные гипотезы"]
    values = [valid_tests, invalid_tests]

    # Круговая диаграмма успешности гипотез
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%",
            colors=["green", "red"], startangle=140)
    plt.title("Распределение гипотез Аполлона")
    plt.show()


if __name__ == "__main__":
    plot_progress()
