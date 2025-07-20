import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, API_KEY
import random
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()

# API ключ для OpenWeatherMap
OWM_API_KEY = API_KEY


@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)


@dp.message(Command('photo'))
async def photo(message: Message):
    photo_urls = [
        'https://i.pinimg.com/originals/d6/d6/0c/d6d60cd014d95b15a5a44cc0597f5947.jpg',
        'https://i.pinimg.com/736x/e6/9b/6f/e69b6feb89a524682cf149d527026893.jpg',
        'https://i.pinimg.com/originals/b5/90/b2/b590b2ed84ff824dd6276fe56b901c13.jpg'
    ]
    rand_photo = random.choice(photo_urls)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('weather'))
async def handle_weather(message: Message):
    await message.answer("🌤️ Отправьте название города для получения прогноза погоды")


def get_weather_info(city):
    """Получает информацию о погоде"""
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru'
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return "❌ Город не найден"

        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        return f"🌤️ *Погода в {city}:*\n🌡️ {temp}°C, {desc}\n💧 Влажность: {humidity}%\n💨 Ветер: {wind} м/с"

    except Exception as e:
        return "❌ Ошибка получения прогноза погоды"


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/weather\n\nТакже можете отправить название города для получения погоды")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")


# Обработчик текстовых сообщений для погоды
@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.strip()

    # Игнорируем команды и специальные сообщения
    if text.startswith('/') or text == "что такое ИИ?":
        return

    # Если сообщение слишком короткое, игнорируем
    if len(text) < 2:
        return

    # Обрабатываем как запрос погоды
    weather_info = get_weather_info(text)
    await message.answer(weather_info, parse_mode='Markdown')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())