import requests
import time
import hashlib
import hmac
import json


class BybitAPI:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        if testnet:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"

    def generate_signature(self, params, timestamp):
        """Генерация подписи для аутентификации"""
        param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        param_str = f"{timestamp}{self.api_key}{param_str}"
        return hmac.new(
            self.api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def make_request(self, endpoint, method="GET", params=None):
        """Отправка запроса к API"""
        if params is None:
            params = {}

        timestamp = str(int(time.time() * 1000))
        signature = self.generate_signature(params, timestamp)

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{endpoint}"

        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        else:
            response = requests.post(url, json=params, headers=headers)

        return response.json()

    def place_order(self, category, symbol, side, orderType, qty, price=None):
        """Размещение ордера"""
        endpoint = "/v5/order/create"

        params = {
            "category": category,  # "linear" для USDT perpetual
            "symbol": symbol,  # "BTCUSDT"
            "side": side,  # "Buy" или "Sell"
            "orderType": orderType,  # "Market" или "Limit"
            "qty": str(qty)
        }

        if price and orderType == "Limit":
            params["price"] = str(price)

        return self.make_request(endpoint, "POST", params)

    def get_positions(self, category="linear"):
        """Получение позиций"""
        endpoint = "/v5/position/list"
        params = {"category": category}
        return self.make_request(endpoint, "GET", params)

    def get_balance(self, accountType="UNIFIED"):
        """Получение баланса"""
        endpoint = "/v5/account/wallet-balance"
        params = {"accountType": accountType}
        return self.make_request(endpoint, "GET", params)


# Пример использования
if __name__ == "__main__":
    # ВНИМАНИЕ: Используйте API ключи из тестовой сети для безопасности!
    API_KEY = "your_api_key_here"
    API_SECRET = "your_api_secret_here"

    # Создание клиента (testnet=True для тестовой сети)
    client = BybitAPI(API_KEY, API_SECRET, testnet=True)

    # Пример: размещение рыночного ордера на покупку BTC
    try:
        order_result = client.place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty=0.001  # Количество BTC
        )
        print("Результат ордера:", json.dumps(order_result, indent=2))

        # Проверка баланса
        balance = client.get_balance()
        print("Баланс:", json.dumps(balance, indent=2))

        # Проверка позиций
        positions = client.get_positions()
        print("Позиции:", json.dumps(positions, indent=2))

    except Exception as e:
        print(f"Ошибка: {e}")