import tkinter as tk
from tkinter import scrolledtext
import apollo_core  # Подключаем основной модуль Аполлона


def send_message():
    """Обрабатывает отправку сообщения в чат."""
    user_message = entry.get()
    if not user_message.strip():
        return

    chat_history.insert(tk.END, f"Ты: {user_message}\n", "user")
    chat_history.yview(tk.END)  # Прокручиваем вниз

    # Передаём запрос в Аполлона и получаем ответ
    apollo_response = apollo_core.process_message(user_message)

    chat_history.insert(tk.END, f"Аполлон: {apollo_response}\n", "apollo")
    chat_history.yview(tk.END)  # Прокручиваем вниз
    entry.delete(0, tk.END)


# Создаём графическое окно
root = tk.Tk()
root.title("Apollo AI Chat")
root.geometry("500x600")

# Окно с историей сообщений
chat_history = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=60, height=25, font=("Arial", 12))
chat_history.pack(pady=10, padx=10)
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("apollo", foreground="green")

# Поле ввода и кнопка отправки
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5)

send_button = tk.Button(root, text="Отправить", command=send_message)
send_button.pack(pady=5)

# Запуск окна
root.mainloop()
