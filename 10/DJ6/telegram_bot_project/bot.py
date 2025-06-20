import asyncio
import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "7575779990:AAFoDQB-YO3EnkKjf-bSazm7IAENv5YG3X8"  # Замените на токен вашего бота
API_BASE_URL = "http://127.0.0.1:8000/api"  # URL Django API

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class APIClient:
    """Клиент для работы с Django API"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def get_session(self):
        """Получение HTTP сессии"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self):
        """Закрытие HTTP сессии"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_user_info(self, telegram_id: int):
        """Получение информации о пользователе"""
        session = await self.get_session()
        url = f"{self.base_url}/user/{telegram_id}/"

        try:
            async with session.get(url) as response:
                data = await response.json()
                return {
                    'status_code': response.status,
                    'data': data
                }
        except Exception as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            return {
                'status_code': 500,
                'data': {'success': False, 'error': str(e)}
            }

    async def register_user(self, user_data: dict):
        """Регистрация пользователя"""
        session = await self.get_session()
        url = f"{self.base_url}/register/"

        try:
            async with session.post(url, json=user_data) as response:
                data = await response.json()
                return {
                    'status_code': response.status,
                    'data': data
                }
        except Exception as e:
            logger.error(f"Ошибка при регистрации пользователя: {e}")
            return {
                'status_code': 500,
                'data': {'success': False, 'error': str(e)}
            }


# Создание экземпляра API клиента
api_client = APIClient(API_BASE_URL)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user = message.from_user

    # Регистрируем пользователя при первом запуске
    user_data = {
        'telegram_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    response = await api_client.register_user(user_data)

    welcome_text = f"""Привет, {user.first_name}! 👋

Я бот для демонстрации интеграции с Django API.

Доступные команды:
/myinfo - получить информацию о вашем профиле
/help - показать справку

Вы были автоматически зарегистрированы в системе!"""

    await message.answer(welcome_text)


@dp.message(Command("myinfo"))
async def cmd_myinfo(message: Message):
    """Обработчик команды /myinfo"""
    user = message.from_user

    # Отправляем сообщение о загрузке
    loading_message = await message.answer("🔄 Получаю информацию...")

    # Запрашиваем данные через API
    response = await api_client.get_user_info(user.id)

    if response['status_code'] == 200 and response['data']['success']:
        user_info = response['data']['user']

        info_text = f"""📋 <b>Информация о пользователе:</b>

🆔 <b>Telegram ID:</b> <code>{user_info['telegram_id']}</code>
👤 <b>Имя пользователя:</b> @{user_info['username'] or 'не указано'}
📝 <b>Имя:</b> {user_info['first_name'] or 'не указано'}
📝 <b>Фамилия:</b> {user_info['last_name'] or 'не указано'}
📛 <b>Полное имя:</b> {user_info['full_name'] or 'не указано'}
✅ <b>Статус:</b> {'Активен' if user_info['is_active'] else 'Неактивен'}
📅 <b>Дата регистрации:</b> {user_info['created_at'][:10]}
🕐 <b>Последняя активность:</b> {user_info['last_seen'][:10]}"""

        await loading_message.edit_text(info_text, parse_mode=ParseMode.HTML)

    elif response['status_code'] == 404:
        error_text = """❌ <b>Пользователь не найден</b>

Вы не зарегистрированы в системе.
Используйте команду /start для регистрации."""
        await loading_message.edit_text(error_text, parse_mode=ParseMode.HTML)

    else:
        error_text = f"""⚠️ <b>Ошибка сервера</b>

Не удалось получить информацию о пользователе.
Код ошибки: {response['status_code']}

Попробуйте позже или обратитесь к администратору."""
        await loading_message.edit_text(error_text, parse_mode=ParseMode.HTML)


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """📖 <b>Справка по командам:</b>

/start - запуск бота и регистрация
/myinfo - получить информацию о профиле
/help - показать эту справку

🔧 <b>О боте:</b>
Этот бот демонстрирует интеграцию Telegram бота с Django API.
Все данные пользователей хранятся в базе данных Django."""

    await message.answer(help_text, parse_mode=ParseMode.HTML)


@dp.message()
async def echo_handler(message: Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "Я не понимаю эту команду. Используйте /help для получения списка доступных команд."
    )


async def main():
    """Главная функция запуска бота"""
    logger.info("Запуск бота...")

    try:
        # Запуск бота
        await dp.start_polling(bot)
    finally:
        # Закрытие сессии
        await api_client.close_session()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())