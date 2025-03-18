import schedule
import time
import os


def run_finance_analysis():
    """Запускает финансовый анализ"""
    print("🚀 Запускаю анализ финансовых данных...")
    os.system("python finance_ai.py")


# Планируем запуск каждый день в 12:00 (можно изменить)
schedule.every().day.at("12:00").do(run_finance_analysis)

print("✅ Планировщик запущен! Финансовый анализ будет выполняться автоматически.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка каждую минуту
