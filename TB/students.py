import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import TOKEN
import sqlite3

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class StudentForm(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


# Инициализируем базу данных при запуске
init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Давайте зарегистрируем вас как ученика.\nКак вас зовут?")
    await state.set_state(StudentForm.name)


@dp.message(StudentForm.name)
async def get_name(message: Message, state: FSMContext):
    # Проверяем, что имя не пустое
    if not message.text.strip():
        await message.answer("Пожалуйста, введите корректное имя:")
        return

    await state.update_data(name=message.text.strip())
    await message.answer("Сколько вам лет?")
    await state.set_state(StudentForm.age)


@dp.message(StudentForm.age)
async def get_age(message: Message, state: FSMContext):
    try:
        age_value = int(message.text)
        # Проверяем разумные границы возраста для школьника
        if age_value < 5 or age_value > 20:
            await message.answer("Пожалуйста, введите корректный возраст школьника (от 5 до 20 лет):")
            return

        await state.update_data(age=age_value)
        await message.answer("В каком классе вы учитесь? (например: 1А, 5Б, 11В)")
        await state.set_state(StudentForm.grade)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (число):")


@dp.message(StudentForm.grade)
async def get_grade(message: Message, state: FSMContext):
    # Проверяем, что класс не пустой
    if not message.text.strip():
        await message.answer("Пожалуйста, введите корректный класс:")
        return

    await state.update_data(grade=message.text.strip())
    user_data = await state.get_data()

    try:
        # Сохраняем данные в базу данных
        conn = sqlite3.connect('school_data.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
        ''', (user_data['name'], user_data['age'], user_data['grade']))
        conn.commit()
        student_id = cur.lastrowid  # Получаем ID созданной записи
        conn.close()

        # Отправляем подтверждение
        await message.answer(
            f"✅ Отлично! Ваши данные успешно сохранены в школьной базе данных:\n\n"
            f"📋 ID ученика: {student_id}\n"
            f"👤 Имя: {user_data['name']}\n"
            f"🎂 Возраст: {user_data['age']} лет\n"
            f"🏫 Класс: {user_data['grade']}\n\n"
            f"Спасибо за регистрацию! 🎓"
        )

    except sqlite3.Error as e:
        await message.answer("❌ Произошла ошибка при сохранении данных. Попробуйте еще раз.")
        logging.error(f"Database error: {e}")

    finally:
        # Очищаем состояние
        await state.clear()


# Дополнительная команда для просмотра статистики (опционально)
@dp.message(Command('stats'))
async def show_stats(message: Message):
    try:
        conn = sqlite3.connect('school_data.db')
        cur = conn.cursor()

        # Получаем общее количество учеников
        cur.execute('SELECT COUNT(*) FROM students')
        total_students = cur.fetchone()[0]

        # Получаем количество учеников по классам
        cur.execute('SELECT grade, COUNT(*) FROM students GROUP BY grade ORDER BY grade')
        grade_stats = cur.fetchall()

        conn.close()

        stats_message = f"📊 Статистика школьной базы данных:\n\n"
        stats_message += f"👥 Всего учеников: {total_students}\n\n"

        if grade_stats:
            stats_message += "📚 По классам:\n"
            for grade, count in grade_stats:
                stats_message += f"  • {grade}: {count} уч.\n"
        else:
            stats_message += "Пока нет зарегистрированных учеников."

        await message.answer(stats_message)

    except sqlite3.Error as e:
        await message.answer("❌ Ошибка при получении статистики")
        logging.error(f"Database error in stats: {e}")


async def main():
    logging.info("Запуск школьного бота...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())