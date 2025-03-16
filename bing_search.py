from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_bing(query):
    """Ищет в Bing через реальный браузер (Selenium) и получает ссылки."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без интерфейса
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    url = f"https://www.bing.com/search?q={query}"
    driver.get(url)

    time.sleep(5)  # Даем больше времени на загрузку

    print("✅ Поиск выполнен успешно!")

    links = []
    results = driver.find_elements(By.CSS_SELECTOR, "h2 a")

    for result in results:
        href = result.get_attribute("href")
        if href and "bing.com" not in href and "microsoft.com" not in href:
            links.append(href)

    driver.quit()

    return links  # Возвращаем список ссылок


if __name__ == "__main__":
    found_links = search_bing("новые технологии AI 2025")
    if found_links:
        print("\n🔗 Найденные ссылки:")
        for link in found_links[:10]:  # Выведем первые 10 ссылок
            print(link)
    else:
        print("❌ Ссылки не найдены!")
