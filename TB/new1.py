import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN  # Убедитесь, что у вас есть файл config.py с TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Создание простого меню с кнопками
# Клавиатура для команды /start
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Задание 2: Кнопки с URL-ссылками
# Инлайн-клавиатура для команды /links
links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📰 Новости", url="https://www.bbc.com/russian")],
        [InlineKeyboardButton(text="🎵 Музыка", url="https://open.spotify.com")],
        [InlineKeyboardButton(text="📹 Видео", url="https://www.youtube.com")]
    ]
)

# Задание 3: Динамическое изменение клавиатуры
# Начальная клавиатура с одной кнопкой
dynamic_keyboard_initial = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Показать больше", callback_data="show_more")]
    ]
)

# Расширенная клавиатура с двумя опциями
dynamic_keyboard_expanded = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="⭐ Опция 2", callback_data="option_2")]
    ]
)

# Обработчик команды /start (Задание 1)
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}! 👋\n"
        f"Выберите одну из кнопок ниже:",
        reply_markup=start_keyboard
    )

# Обработчик команды /links (Задание 2)
@dp.message(Command('links'))
async def links_command(message: Message):
    await message.answer(
        "🔗 Выберите категорию ссылок:",
        reply_markup=links_keyboard
    )

# Обработчик команды /dynamic (Задание 3)
@dp.message(Command('dynamic'))
async def dynamic_command(message: Message):
    await message.answer(
        "🔄 Динамическое меню:\n"
        "Нажмите кнопку ниже, чтобы увидеть больше опций!",
        reply_markup=dynamic_keyboard_initial
    )

# Обработчики callback-запросов для динамической клавиатуры (Задание 3)
@dp.callback_query(F.data == "show_more")
async def show_more_options(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔄 Динамическое меню:\n"
        "Теперь у вас есть две опции на выбор!",
        reply_markup=dynamic_keyboard_expanded
    )
    await callback.answer("Показано больше опций! 🎉")

@dp.callback_query(F.data == "option_1")
async def select_option_1(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ Вы выбрали Опцию 1!\n"
        "Отличный выбор! 👍"
    )
    await callback.answer("Выбрана Опция 1!")

@dp.callback_query(F.data == "option_2")
async def select_option_2(callback: CallbackQuery):
    await callback.message.edit_text(
        "⭐ Вы выбрали Опцию 2!\n"
        "Превосходный выбор! ⭐"
    )
    await callback.answer("Выбрана Опция 2!")

# Обработчики для кнопок меню (Задание 1)
@dp.message(F.text == "Привет")
async def hello_button(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! 😊")

@dp.message(F.text == "Пока")
async def goodbye_button(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"До свидания, {user_name}! 👋")

# Дополнительный обработчик команды /help для удобства
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "🤖 Доступные команды:\n"
        "/start - Показать главное меню с кнопками\n"
        "/links - Показать меню с полезными ссылками\n"
        "/dynamic - Показать динамическое меню\n"
        "/help - Показать это сообщение\n\n"
        "Просто нажимайте на кнопки для взаимодействия с ботом!"
    )

# Обработчик для всех остальных текстовых сообщений
@dp.message(F.text)
async def handle_other_messages(message: Message):
    await message.answer(
        "🤔 Я не понимаю это сообщение.\n"
        "Используйте кнопки меню или команды /start, /links, /help"
    )

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())