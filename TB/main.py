import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, API_KEY
import random
import requests
import os
from gtts import gTTS
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()

# API ключ для OpenWeatherMap
OWM_API_KEY = API_KEY

# Инициализация переводчика
translator = Translator()

if not os.path.exists('img'):
    os.makedirs('img')


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound2.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("doc.pdf")
    await bot.send_document(message.chat.id, doc)


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)


@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(Command('photos', prefix='&'))
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


@dp.message(Command('translate'))
async def translate_command(message: Message):
    await message.answer("🔄 Отправьте текст для перевода на английский язык")


def translate_to_english(text):
    """Переводит текст на английский язык"""
    try:
        # Определяем язык исходного текста
        detected = translator.detect(text)

        # Если текст уже на английском, возвращаем его как есть
        if detected.lang == 'en':
            return f"🔄 Текст уже на английском языке:\n{text}"

        # Переводим на английский
        translated = translator.translate(text, dest='en')

        return f"🔄 *Перевод на английский:*\n\n📝 *Оригинал ({detected.lang}):*\n{text}\n\n🇺🇸 *Перевод:*\n{translated.text}"

    except Exception as e:
        return f"❌ Ошибка перевода: {str(e)}"


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


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n/start - начало работы\n/help - помощь\n/photo - фото\n/weather - погода\n/translate - перевод текста\n\nТакже можете:\n• Отправить название города для получения погоды\n• Отправить любой текст для перевода на английский")


# Обработчик текстовых сообщений
@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.strip()

    # Игнорируем команды и специальные сообщения
    if text.startswith('/') or text == "что такое ИИ?":
        return

    # Если сообщение слишком короткое, игнорируем
    if len(text) < 2:
        return

    # Проверяем, может ли это быть названием города для погоды
    # Простая эвристика: короткие сообщения (до 30 символов) без знаков препинания
    if len(text) <= 30 and not any(char in text for char in '.,!?;:"\'()[]{}'):
        # Пробуем получить погоду
        weather_info = get_weather_info(text)

        # Если город найден (не содержит "не найден"), отправляем погоду
        if "не найден" not in weather_info.lower():
            await message.answer(weather_info, parse_mode='Markdown')
            return

    # Если это не город или город не найден, переводим текст
    translation = translate_to_english(text)
    await message.answer(translation, parse_mode='Markdown')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())