import requests


def search_duckduckgo(query):
    """Ищет информацию через DuckDuckGo API."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    print(f"🔍 Отправляю запрос: {url}")  # Проверяем, что запрос формируется
    response = requests.get(url)

    if response.status_code == 200:
        print("✅ Успешный ответ!")  # Проверяем, получаем ли мы ответ
        data = response.json()
        results = []

        if 'RelatedTopics' in data:
            for topic in data['RelatedTopics']:
                if 'Text' in topic and 'FirstURL' in topic:
                    results.append({
                        'title': topic['Text'],
                        'link': topic['FirstURL']
                    })

        return results
    else:
        print(f"⚠️ Ошибка! Код ответа: {response.status_code}")
        return []


if __name__ == "__main__":
    query = "новые технологии AI"
    results = search_duckduckgo(query)

    if results:
        for res in results:
            print(f"{res['title']} - {res['link']}")
    else:
        print("❌ Ничего не найдено.")
