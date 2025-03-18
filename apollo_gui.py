import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import apollo_core  # Подключаем основной модуль Аполлона


def send_message(event=None):
    """Обрабатывает отправку сообщения в чат."""
    user_message = entry.get()
    if not user_message.strip():
        return

    chat_history.insert(tk.END, f"\n🟦 Ты: {user_message}\n", "user")
    chat_history.yview(tk.END)  # Прокрутка вниз

    # Передаём запрос в Аполлона и получаем ответ
    apollo_response = apollo_core.process_message(user_message)

    chat_history.insert(tk.END, f"🟩 Аполлон: {apollo_response}\n", "apollo")
    chat_history.yview(tk.END)  # Прокрутка вниз
    entry.delete(0, tk.END)
    entry.focus()  # Возвращаем фокус на поле ввода


# Создаём графическое окно
root = tk.Tk()
root.title("Apollo AI Chat")
root.geometry("600x700")
root.configure(bg="#1e1e1e")  # Тёмный фон

# Окно с историей сообщений
chat_history = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=70, height=25, font=("Arial", 14),
    bg="#282c34", fg="white", insertbackground="white", borderwidth=0, relief=tk.FLAT
)
chat_history.pack(pady=10, padx=10)
chat_history.tag_config("user", foreground="#61afef",
                        font=("Arial", 14, "bold"))
chat_history.tag_config("apollo", foreground="#98c379",
                        font=("Arial", 14, "bold"))

# Поле ввода
entry = tk.Entry(root, width=55, font=("Arial", 14),
                 bg="#3e4451", fg="white", insertbackground="white")
entry.pack(pady=5, padx=10, ipady=5)
entry.bind("<Return>", send_message)  # Обработка Enter

# Кнопка отправки
send_button = tk.Button(root, text="🚀 Отправить", command=send_message, font=("Arial", 14, "bold"),
                        bg="#61afef", fg="white", relief=tk.FLAT, cursor="hand2")
send_button.pack(pady=10)

# Автофокус на поле ввода
entry.focus()

# Запуск окна
root.mainloop()
