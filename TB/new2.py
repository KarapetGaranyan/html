import asyncio
import requests
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, NASA_API_KEY, THE_CAT_API_KEY, WEATHER_API_KEY, QUOTES_API_KEY

# Инициализация бота
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния для FSM
class WeatherStates(StatesGroup):
    waiting_for_city = State()


class QuoteStates(StatesGroup):
    waiting_for_category = State()


# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 Кошки", callback_data="cats_menu")],
        [InlineKeyboardButton(text="🌌 NASA APOD", callback_data="nasa_apod")],
        [InlineKeyboardButton(text="🌤️ Погода", callback_data="weather")],
        [InlineKeyboardButton(text="💭 Цитаты", callback_data="quotes")],
        [InlineKeyboardButton(text="🎲 Случайное число", callback_data="random_number")],
        [InlineKeyboardButton(text="📊 Информация о боте", callback_data="bot_info")]
    ])
    return keyboard


# Меню для кошек
def get_cats_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 Случайная кошка", callback_data="random_cat")],
        [InlineKeyboardButton(text="🔍 Поиск по породе", callback_data="search_breed")],
        [InlineKeyboardButton(text="📋 Список пород", callback_data="list_breeds")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    return keyboard


# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С API ==========

# NASA API функции
def get_random_apod():
    """Получение случайного APOD от NASA"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'

    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except requests.RequestException:
        return None


def get_today_apod():
    """Получение APOD на сегодня"""
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'

    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except requests.RequestException:
        return None


# Cat API функции
def get_cat_breeds():
    """Получение списка пород кошек"""
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except requests.RequestException:
        return []


def get_random_cat():
    """Получение случайной картинки кошки"""
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {"x-api-key": THE_CAT_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return data[0]['url'] if data else None
    except requests.RequestException:
        return None


def get_cat_image_by_breed(breed_id):
    """Получение картинки кошки по породе"""
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return data[0]['url'] if data else None
    except requests.RequestException:
        return None


def get_breed_info(breed_name):
    """Получение информации о породе кошек"""
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


# Погода API (OpenWeatherMap)
def get_weather(city):
    """Получение информации о погоде"""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except requests.RequestException:
        return None


# Цитаты API (несколько источников для надежности)
def get_random_quote():
    """Получение случайной цитаты из разных источников"""

    # Локальные цитаты как fallback
    local_quotes = [
        {"content": "Будь собой. Остальные роли уже заняты.", "author": "Оскар Уайльд"},
        {"content": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон"},
        {"content": "Единственный способ делать отличную работу — любить то, что делаешь.", "author": "Стив Джобс"},
        {"content": "Будущее принадлежит тем, кто верит в красоту своих мечтаний.", "author": "Элеанор Рузвельт"},
        {"content": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.",
         "author": "Уинстон Черчилль"},
        {"content": "Не важно, насколько медленно ты идешь, главное — не останавливаться.", "author": "Конфуций"},
        {"content": "Лучшее время для посадки дерева было 20 лет назад. Второе лучшее время — сейчас.",
         "author": "Китайская пословица"},
        {"content": "Измените свои мысли, и вы измените свой мир.", "author": "Норман Винсент Пил"},
        {"content": "Дорогу осилит идущий.", "author": "Русская пословица"},
        {"content": "Мечты не работают, пока не работаешь ты.", "author": "Джон К. Максвелл"}
    ]

    # Пытаемся получить цитату из API
    apis_to_try = [
        {
            "url": "https://zenquotes.io/api/random",
            "parser": lambda x: {"content": x[0]["q"], "author": x[0]["a"]} if x and isinstance(x, list) and len(
                x) > 0 else None
        },
        {
            "url": "https://api.quotable.io/random",
            "parser": lambda x: {"content": x["content"], "author": x["author"]} if x and "content" in x else None
        },
        {
            "url": "https://api.adviceslip.com/advice",
            "parser": lambda x: {"content": x["slip"]["advice"], "author": "Совет дня"} if x and "slip" in x else None
        }
    ]

    for api in apis_to_try:
        try:
            response = requests.get(api["url"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                parsed = api["parser"](data)
                if parsed:
                    return parsed
        except:
            continue

    # Если все API недоступны, возвращаем случайную локальную цитату
    return random.choice(local_quotes)


def get_inspirational_quote():
    """Получение вдохновляющей цитаты"""
    inspirational_quotes = [
        {"content": "Верьте в себя и в то, что вы можете сделать невозможное возможным.",
         "author": "Мотивационная мудрость"},
        {"content": "Каждый день — это новая возможность изменить свою жизнь.", "author": "Жизненная философия"},
        {"content": "Самые темные часы наступают прямо перед рассветом.", "author": "Томас Фуллер"},
        {"content": "Если вы можете мечтать об этом, вы можете это сделать.", "author": "Уолт Дисней"},
        {"content": "Единственное невозможное путешествие — это то, которое вы никогда не начинаете.",
         "author": "Тони Роббинс"}
    ]

    # Пытаемся получить вдохновляющую цитату из API
    try:
        response = requests.get("https://zenquotes.io/api/today", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                return {"content": data[0]["q"], "author": data[0]["a"]}
    except:
        pass

    return random.choice(inspirational_quotes)


# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(CommandStart())
async def start_command(message: Message):
    welcome_text = """
🤖 Добро пожаловать в многофункционального бота!

Вот что я умею:
🐱 Показывать информацию о кошках и их породах
🌌 Присылать космические фото от NASA
🌤️ Узнавать погоду в любом городе
💭 Делиться мудрыми цитатами
🎲 Генерировать случайные числа

Выберите функцию из меню ниже:
    """
    await message.answer(welcome_text, reply_markup=get_main_menu())


@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = """
📚 Доступные команды:

/start - Главное меню
/help - Это сообщение
/random_cat - Случайная кошка
/random_apod - Случайное фото космоса
/weather - Узнать погоду
/quote - Случайная цитата
/inspiration - Вдохновляющая цитата

Или используйте интерактивное меню!
    """
    await message.answer(help_text)


# ========== ОБРАБОТЧИКИ CALLBACK ЗАПРОСОВ ==========

@dp.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 Главное меню\n\nВыберите нужную функцию:",
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == "cats_menu")
async def cats_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🐱 Меню кошек\n\nВыберите действие:",
        reply_markup=get_cats_menu()
    )


@dp.callback_query(F.data == "random_cat")
async def random_cat_callback(callback: CallbackQuery):
    cat_url = get_random_cat()
    if cat_url:
        await callback.message.answer_photo(
            photo=cat_url,
            caption="🐱 Случайная кошечка для вас!"
        )
    else:
        await callback.message.answer("❌ Не удалось получить изображение кошки")


@dp.callback_query(F.data == "nasa_apod")
async def nasa_apod_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Сегодня", callback_data="apod_today")],
        [InlineKeyboardButton(text="🎲 Случайное", callback_data="apod_random")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])

    await callback.message.edit_text(
        "🌌 NASA Astronomy Picture of the Day\n\nВыберите опцию:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "apod_today")
async def apod_today_callback(callback: CallbackQuery):
    apod = get_today_apod()
    if apod and 'url' in apod:
        caption = f"🌌 {apod['title']}\n\n{apod.get('explanation', '')[:200]}..."
        await callback.message.answer_photo(photo=apod['url'], caption=caption)
    else:
        await callback.message.answer("❌ Не удалось получить изображение NASA")


@dp.callback_query(F.data == "apod_random")
async def apod_random_callback(callback: CallbackQuery):
    apod = get_random_apod()
    if apod and 'url' in apod:
        caption = f"🌌 {apod['title']}\n📅 {apod.get('date', '')}\n\n{apod.get('explanation', '')[:200]}..."
        await callback.message.answer_photo(photo=apod['url'], caption=caption)
    else:
        await callback.message.answer("❌ Не удалось получить изображение NASA")


@dp.callback_query(F.data == "weather")
async def weather_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🌤️ Введите название города для получения прогноза погоды:")
    await state.set_state(WeatherStates.waiting_for_city)


@dp.callback_query(F.data == "quotes")
async def quotes_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Случайная цитата", callback_data="random_quote")],
        [InlineKeyboardButton(text="✨ Вдохновляющая", callback_data="inspirational_quote")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])

    await callback.message.edit_text(
        "💭 Цитаты и мудрость\n\nВыберите тип цитаты:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "random_quote")
async def random_quote_callback(callback: CallbackQuery):
    quote = get_random_quote()
    if quote:
        text = f"💭 \"{quote['content']}\"\n\n© {quote['author']}"
        await callback.message.answer(text)
    else:
        await callback.message.answer("❌ Не удалось получить цитату")


@dp.callback_query(F.data == "inspirational_quote")
async def inspirational_quote_callback(callback: CallbackQuery):
    quote = get_inspirational_quote()
    if quote:
        text = f"✨ \"{quote['content']}\"\n\n© {quote['author']}"
        await callback.message.answer(text)
    else:
        await callback.message.answer("❌ Не удалось получить цитату")


@dp.callback_query(F.data == "random_number")
async def random_number_callback(callback: CallbackQuery):
    number = random.randint(1, 100)
    await callback.message.answer(f"🎲 Ваше случайное число: {number}")


@dp.callback_query(F.data == "bot_info")
async def bot_info_callback(callback: CallbackQuery):
    info_text = """
📊 Информация о боте:

🔧 Версия: 2.0
🚀 Использует aiogram 3
🌐 API сервисы:
  • NASA APOD API
  • The Cat API
  • OpenWeatherMap API
  • Quotable API

👨‍💻 Создан для демонстрации работы с различными API
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    await callback.message.edit_text(info_text, reply_markup=keyboard)


@dp.callback_query(F.data == "list_breeds")
async def list_breeds_callback(callback: CallbackQuery):
    breeds = get_cat_breeds()
    if breeds:
        breed_names = [breed['name'] for breed in breeds[:20]]  # Показываем только первые 20
        breeds_text = "🐱 Популярные породы кошек:\n\n" + "\n".join(f"• {name}" for name in breed_names)
        breeds_text += f"\n\n... и ещё {len(breeds) - 20} пород!" if len(breeds) > 20 else ""
        await callback.message.answer(breeds_text)
    else:
        await callback.message.answer("❌ Не удалось получить список пород")


# ========== ОБРАБОТЧИКИ СОСТОЯНИЙ ==========

@dp.message(WeatherStates.waiting_for_city)
async def process_city_weather(message: Message, state: FSMContext):
    city = message.text
    weather_data = get_weather(city)

    if weather_data and weather_data.get('cod') == 200:
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        weather_text = f"""
🌤️ Погода в городе {city}:

🌡️ Температура: {temp}°C
🌡️ Ощущается как: {feels_like}°C
📝 Описание: {description}
💧 Влажность: {humidity}%
        """
        await message.answer(weather_text)
    else:
        await message.answer("❌ Город не найден. Попробуйте еще раз или используйте /start для возврата в меню.")

    await state.clear()


# ========== ТЕКСТОВЫЕ СООБЩЕНИЯ ==========

@dp.message(F.text)
async def handle_text_messages(message: Message):
    text = message.text.lower()

    # Проверяем, не является ли это поиском породы кошки
    breed_info = get_breed_info(message.text)
    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info['id'])

        info = (
            f"🐱 **{breed_info['name']}**\n\n"
            f"🌍 Происхождение: {breed_info['origin']}\n"
            f"📝 Описание: {breed_info['description']}\n"
            f"😸 Темперамент: {breed_info['temperament']}\n"
            f"⏳ Продолжительность жизни: {breed_info['life_span']} лет"
        )

        if cat_image_url:
            await message.answer_photo(photo=cat_image_url, caption=info)
        else:
            await message.answer(info)
    else:
        # Если порода не найдена, предлагаем использовать меню
        await message.answer(
            "🤔 Я не понимаю эту команду или не нашел такую породу кошек.\n"
            "Используйте /start для вызова главного меню!",
            reply_markup=get_main_menu()
        )


# ========== КОМАНДЫ ДЛЯ БЫСТРОГО ДОСТУПА ==========

@dp.message(Command("random_cat"))
async def random_cat_command(message: Message):
    cat_url = get_random_cat()
    if cat_url:
        await message.answer_photo(photo=cat_url, caption="🐱 Случайная кошечка!")
    else:
        await message.answer("❌ Не удалось получить изображение кошки")


@dp.message(Command("random_apod"))
async def random_apod_command(message: Message):
    apod = get_random_apod()
    if apod and 'url' in apod:
        caption = f"🌌 {apod['title']}\n📅 {apod.get('date', '')}"
        await message.answer_photo(photo=apod['url'], caption=caption)
    else:
        await message.answer("❌ Не удалось получить изображение NASA")


@dp.message(Command("weather"))
async def weather_command(message: Message, state: FSMContext):
    await message.answer("🌤️ Введите название города:")
    await state.set_state(WeatherStates.waiting_for_city)


@dp.message(Command("quote"))
async def quote_command(message: Message):
    quote = get_random_quote()
    if quote:
        text = f"💭 \"{quote['content']}\"\n\n© {quote['author']}"
        await message.answer(text)
    else:
        await message.answer("❌ Не удалось получить цитату")


@dp.message(Command("inspiration"))
async def inspiration_command(message: Message):
    quote = get_inspirational_quote()
    if quote:
        text = f"✨ \"{quote['content']}\"\n\n© {quote['author']}"
        await message.answer(text)
    else:
        await message.answer("❌ Не удалось получить цитату")


# ========== ЗАПУСК БОТА ==========

async def main():
    print("🚀 Бот запущен!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())