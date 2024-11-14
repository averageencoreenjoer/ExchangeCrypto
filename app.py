from flask import Flask, request, jsonify
from flask_cors import CORS  # Для поддержки CORS
import requests
import time

app = Flask(__name__)

# Включаем CORS для всех маршрутов
CORS(app)

# Переменная для хранения кешированных данных
cache = {}
cache_time = 60  # Время хранения кэшированных данных (в секундах)

# Словарь для преобразования сокращений в идентификаторы
currency_map = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'usdt': 'tether',
    # Добавьте другие криптовалюты по необходимости
}

# Функция для получения актуальных курсов криптовалюты
def get_exchange_rate(from_currency, to_currency):
    # Ключ для хранения кэшированных данных
    cache_key = f"{from_currency}_{to_currency}"
    current_time = time.time()

    # Проверяем, есть ли в кэше актуальные данные
    if cache_key in cache and current_time - cache[cache_key]["timestamp"] < cache_time:
        print("Returning cached data")
        return cache[cache_key]["rate"]

    # Преобразуем сокращенные валюты в нужные идентификаторы
    from_currency = currency_map.get(from_currency.lower(), from_currency.lower())
    to_currency = to_currency.lower()
    
    # Пример запроса: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_currency}&vs_currencies={to_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        print(f"API response for {from_currency} to {to_currency}: {data}")
        
        # Кэшируем полученные данные
        rate = data.get(from_currency, {}).get(to_currency)
        if rate:
            cache[cache_key] = {"rate": rate, "timestamp": current_time}
        return rate
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.get_json()  # Получаем данные из запроса
    print("Received data:", data)  # Логируем полученные данные

    # Извлекаем параметры из данных
    from_currency = data.get("fromCurrency")
    to_currency = data.get("toCurrency")
    amount = data.get("amount")

    # Проверяем, что все данные присутствуют и сумма больше нуля
    if not from_currency or not to_currency or amount <= 0:
        return jsonify({"error": "Invalid data"}), 400

    # Получаем курс обмена
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        return jsonify({"error": "Exchange rate not available"}), 400

    # Вычисляем результат обмена
    result = amount * rate
    return jsonify({"result": result})  # Возвращаем результат в JSON

if __name__ == "__main__":
    app.run(debug=True)