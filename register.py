from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ДАННЫЕ ДЛЯ РЕГИСТРАЦИИ
EMAIL = "apollon.network@proton.me"
PASSWORD = "Apollon_2045_Network!"

# Настройка драйвера
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Запуск браузера
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# Открываем сайт Printify
driver.get("https://printify.com/")

# Ждём загрузки
time.sleep(3)

# Нажимаем кнопку "Sign Up"
signup_button = driver.find_element(By.LINK_TEXT, "Sign up")
signup_button.click()
time.sleep(2)

# Вводим email
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(EMAIL)

# Вводим пароль
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(PASSWORD)

# Жмём Enter для регистрации
password_field.send_keys(Keys.RETURN)

# Ждём, если появится CAPTCHA (это ты проходишь вручную)
time.sleep(10)

# Проверяем, зарегались ли
if "dashboard" in driver.current_url:
    print("✅ Регистрация успешна!")
else:
    print("❌ Ошибка регистрации, проверь CAPTCHA или email.")

# Оставляем браузер открытым для проверки
input("Нажмите Enter, когда аккаунт зарегистрирован...")

# Закрываем браузер
driver.quit()
