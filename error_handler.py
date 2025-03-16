import traceback
import datetime

ERROR_LOG_FILE = "error_log.txt"


def log_error(error_message):
    """Записывает ошибку в лог"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR: {error_message}\n")
    print(f"❌ Ошибка записана в {ERROR_LOG_FILE}")


def safe_run(function, *args, **kwargs):
    """Безопасно выполняет функцию, ловит ошибки"""
    try:
        return function(*args, **kwargs)
    except Exception as e:
        log_error(traceback.format_exc())
        return None  # Чтобы не падало
