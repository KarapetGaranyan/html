import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import time
import hashlib
import hmac

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BybitTelegramBot:
    def __init__(self, telegram_token, bybit_api_key, bybit_api_secret, testnet=True):
        self.telegram_token = telegram_token
        self.bybit_api_key = bybit_api_key
        self.bybit_api_secret = bybit_api_secret
        self.testnet = testnet
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"

    def generate_signature(self, params, timestamp):
        """Генерация подписи для Bybit API"""
        param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        param_str = f"{timestamp}{self.bybit_api_key}{param_str}"
        return hmac.new(
            self.bybit_api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def bybit_request(self, endpoint, method="GET", params=None):
        """Отправка запроса к Bybit API"""
        if params is None:
            params = {}

        timestamp = str(int(time.time() * 1000))
        signature = self.generate_signature(params, timestamp)

        headers = {
            "X-BAPI-API-KEY": self.bybit_api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.post(url, json=params, headers=headers)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка API запроса: {e}")
            return {"retCode": -1, "retMsg": str(e)}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        keyboard = [
            [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
            [InlineKeyboardButton("📊 Позиции", callback_data="positions")],
            [InlineKeyboardButton("🔥 Купить BTC", callback_data="buy_btc")],
            [InlineKeyboardButton("📉 Продать BTC", callback_data="sell_btc")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🤖 Добро пожаловать в Bybit Trading Bot!\n\n"
            "Выберите действие:",
            reply_markup=reply_markup
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий кнопок"""
        query = update.callback_query
        await query.answer()

        if query.data == "balance":
            await self.show_balance(query)
        elif query.data == "positions":
            await self.show_positions(query)
        elif query.data == "buy_btc":
            await self.place_order(query, "Buy")
        elif query.data == "sell_btc":
            await self.place_order(query, "Sell")

    async def show_balance(self, query):
        """Показать баланс"""
        result = self.bybit_request("/v5/account/wallet-balance", "GET", {"accountType": "UNIFIED"})

        if result.get("retCode") == 0:
            balances = result["result"]["list"][0]["coin"]
            message = "💰 Ваш баланс:\n\n"

            for coin in balances:
                if float(coin["walletBalance"]) > 0:
                    message += f"{coin['coin']}: {coin['walletBalance']}\n"
        else:
            message = f"❌ Ошибка получения баланса: {result.get('retMsg', 'Неизвестная ошибка')}"

        await query.edit_message_text(message)

    async def show_positions(self, query):
        """Показать позиции"""
        result = self.bybit_request("/v5/position/list", "GET", {"category": "linear"})

        if result.get("retCode") == 0:
            positions = result["result"]["list"]
            message = "📊 Ваши позиции:\n\n"

            active_positions = [pos for pos in positions if float(pos["size"]) != 0]

            if active_positions:
                for pos in active_positions:
                    message += f"{pos['symbol']}: {pos['size']} ({pos['side']})\n"
                    message += f"PnL: {pos['unrealisedPnl']} USDT\n\n"
            else:
                message = "📊 У вас нет открытых позиций"
        else:
            message = f"❌ Ошибка получения позиций: {result.get('retMsg', 'Неизвестная ошибка')}"

        await query.edit_message_text(message)

    async def place_order(self, query, side):
        """Разместить ордер"""
        params = {
            "category": "linear",
            "symbol": "BTCUSDT",
            "side": side,
            "orderType": "Market",
            "qty": "0.001"  # Минимальное количество для теста
        }

        result = self.bybit_request("/v5/order/create", "POST", params)

        if result.get("retCode") == 0:
            order_id = result["result"]["orderId"]
            message = f"✅ Ордер размещен успешно!\n\n"
            message += f"Тип: {side} BTC\n"
            message += f"Количество: 0.001 BTC\n"
            message += f"Order ID: {order_id}"
        else:
            message = f"❌ Ошибка размещения ордера: {result.get('retMsg', 'Неизвестная ошибка')}"

        await query.edit_message_text(message)

    def run(self):
        """Запуск бота"""
        application = Application.builder().token(self.telegram_token).build()

        # Обработчики команд
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.button_handler))

        # Запуск бота
        application.run_polling()


# Использование
if __name__ == "__main__":
    # Замените на ваши реальные токены и ключи
    TELEGRAM_TOKEN = "your_telegram_bot_token"
    BYBIT_API_KEY = "your_bybit_api_key"
    BYBIT_API_SECRET = "your_bybit_api_secret"

    bot = BybitTelegramBot(TELEGRAM_TOKEN, BYBIT_API_KEY, BYBIT_API_SECRET, testnet=True)
    bot.run()