import os
import subprocess

# Названия файлов-скриптов
SELF_ANALYSIS_SCRIPT = "self_analysis.py"
SELF_CORRECTION_SCRIPT = "self_correction.py"
ERROR_RECOVERY_SCRIPT = "error_recovery.py"
HYPOTHESIS_TESTER_SCRIPT = "hypothesis_tester.py"


def run_script(script_name):
    """Запускает внешний Python-скрипт"""
    if os.path.exists(script_name):
        print(f"🔄 Запускаю {script_name}...")
        result = subprocess.run(["python", script_name],
                                capture_output=True, text=True)
        print(result.stdout)
    else:
        print(f"⚠️ Скрипт {script_name} не найден.")


def self_improvement_cycle():
    """Запускает полный цикл самоанализа и самоисправления один раз"""
    print("\n🚀 **Запуск цикла саморазвития Аполлона** 🚀\n")

    run_script(SELF_ANALYSIS_SCRIPT)  # Анализируем ошибки
    run_script(SELF_CORRECTION_SCRIPT)  # Генерируем исправления
    run_script(ERROR_RECOVERY_SCRIPT)  # Откатываем ошибки
    run_script(HYPOTHESIS_TESTER_SCRIPT)  # Тестируем новые гипотезы

    print("\n✅ **Цикл саморазвития завершён.** ✅\n")


if __name__ == "__main__":
    self_improvement_cycle()
