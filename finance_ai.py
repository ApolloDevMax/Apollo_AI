import json
import requests
import datetime
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# API КЛЮЧ (замени на реальный перед запуском)
ALPHA_VANTAGE_API_KEY = "VXZQ84640KBVM1UR"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
MEMORY_FILE = "memory.json"

# ==============================
# 🔥 ФУНКЦИИ ДЛЯ АНАЛИЗА ДАННЫХ
# ==============================


def fetch_crypto_price(symbol):
    """Получает текущую цену криптовалюты по API CoinGecko"""
    try:
        url = f"{COINGECKO_API_URL}?ids={symbol}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data[symbol]["usd"])
    except Exception as e:
        print(f"❌ Ошибка получения цены криптовалюты {symbol}: {e}")
        return None


def load_memory():
    """Загружает память, если файла нет — создаёт его"""
    if not os.path.exists(MEMORY_FILE):
        return {"finance": []}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"finance": []}


def save_to_memory(data):
    """Сохраняет анализ в память"""
    memory = load_memory()
    memory["finance"].append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": data
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

    print("✅ Финансовый анализ сохранён в память!")


def predict_trend(symbol, past_data):
    """Предсказывает тренд на основе прошлых цен (линейная регрессия)"""
    if len(past_data) < 5:
        return "Недостаточно данных"

    X = np.array(range(len(past_data))).reshape(-1, 1)
    y = np.array(past_data)

    model = LinearRegression()
    model.fit(X, y)

    future_price = model.predict(np.array([[len(past_data)]]))[0]
    trend = "Рост" if future_price > y[-1] else "Падение"

    return f"{trend} (прогноз: {future_price:.2f} USD)"


def analyze_trends():
    """Анализирует тренды на основе прошлых данных"""
    memory = load_memory()
    market_trends = {}

    for asset in ["bitcoin", "ethereum", "solana"]:
        past_prices = []
        for entry in memory.get("finance", []):
            if "analysis" in entry and asset in entry["analysis"]:
                past_prices.append(entry["analysis"][asset])

        if past_prices:
            market_trends[asset] = predict_trend(asset, past_prices)

    return market_trends

# ==============================
# 🚀 ЗАПУСК АНАЛИЗА
# ==============================


if __name__ == "__main__":
    print("📊 Запуск финансового анализа...")
    market_trends = analyze_trends()

    if market_trends:
        print(f"📈 Прогнозы рынка: {market_trends}")
        save_to_memory({"trends": market_trends})
    else:
        print("⚠️ Недостаточно данных для предсказаний.")
