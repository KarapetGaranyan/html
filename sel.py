from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import glob
import re
from datetime import datetime
from tkinter import Tk, filedialog


# Функция для получения пути к папке загрузок
def get_downloads_folder():
    # Стандартная папка загрузок для Windows
    return os.path.join(os.path.expanduser('~'), 'Downloads')


# Функция для очистки имени файла от недопустимых символов
def clean_filename(filename):
    # Список недопустимых символов в Windows
    invalid_chars = r'[<>:"/\\|?*]'

    # Заменяем недопустимые символы на пустую строку
    clean_name = re.sub(invalid_chars, '', filename)

    # Удаляем лишние пробелы в начале и конце
    clean_name = clean_name.strip()

    # Проверка на пустое имя после очистки
    if not clean_name:
        clean_name = "Компания"  # Если имя стало пустым, устанавливаем стандартное

    return clean_name


# Функция для поиска и переименования последнего скачанного файла
def rename_latest_file(download_folder, company_name):
    # Очищаем имя компании для использования в имени файла
    safe_name = clean_filename(company_name)

    # Получаем список всех файлов .pdf в папке загрузок
    pdf_files = glob.glob(os.path.join(download_folder, '*.pdf'))

    if not pdf_files:
        print(f"Ошибка: PDF файлы не найдены в {download_folder}")
        return False

    # Получаем самый новый файл по времени создания
    latest_file = max(pdf_files, key=os.path.getctime)

    # Формируем новое имя файла
    new_filename = f"{safe_name}.pdf"
    new_path = os.path.join(download_folder, new_filename)

    # Если файл с таким именем уже существует, добавляем timestamp
    if os.path.exists(new_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{safe_name}_{timestamp}.pdf"
        new_path = os.path.join(download_folder, new_filename)

    try:
        os.rename(latest_file, new_path)
        print(f"Файл переименован в: {new_filename}")
        # Выводим оригинальное и безопасное имя, если они отличаются
        if company_name != safe_name:
            print(f"(Оригинальное имя '{company_name}' было очищено для совместимости с файловой системой)")
        return True
    except Exception as e:
        print(f"Ошибка при переименовании файла: {e}")
        return False


# Функция для удаления кавычек в данных
def remove_quotes(value):
    if isinstance(value, str):
        # Удаляем одинарные и двойные кавычки с начала и конца строки
        return value.strip('\'"')
    return value


# Функция для нормализации ИНН
def normalize_inn(inn_value):
    if pd.isna(inn_value):
        return None

    # Преобразуем в строку в любом случае
    inn_str = str(inn_value).strip()

    # Удаляем все нецифровые символы (если есть)
    inn_digits = re.sub(r'\D', '', inn_str)

    # Проверяем длину и добавляем ведущие нули при необходимости
    if len(inn_digits) < 10:  # Минимальная длина ИНН (ЮЛ)
        # Дополняем до 10 цифр для юридических лиц
        inn_digits = inn_digits.zfill(10)
    elif len(inn_digits) < 12 and len(inn_digits) > 10:
        # Дополняем до 12 цифр для физических лиц
        inn_digits = inn_digits.zfill(12)

    return inn_digits


# Инициализация Tkinter для выбора файла
root = Tk()
root.withdraw()  # Скрываем основное окно Tkinter

# Открываем диалоговое окно выбора файла
print("Пожалуйста, выберите Excel-файл в открывшемся окне...")
excel_file_path = filedialog.askopenfilename(
    title="Выберите Excel-файл",
    filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
)

# Проверяем, был ли выбран файл
if not excel_file_path:
    print("Файл не выбран. Завершение программы.")
    exit(1)

print(f"Выбран файл: {excel_file_path}")

# Чтение данных из Excel с указанием, что все столбцы должны быть строками
try:
    # Читаем Excel с явным указанием типов данных для столбцов
    df = pd.read_excel(
        excel_file_path,
        header=None,
        dtype=str  # Все столбцы читаем как строки, чтобы сохранить ведущие нули
    )

    # Выводим размер датафрейма до обработки
    print(f"Размер прочитанного датафрейма: {df.shape}")

    # Переименовываем столбцы для удобства
    df.columns = ['A', 'B'] + [f'Col{i}' for i in range(2, len(df.columns))]

    # Применяем функцию удаления кавычек к столбцам A и B
    df['A'] = df['A'].apply(remove_quotes)
    df['B'] = df['B'].apply(remove_quotes)

    # Нормализуем ИНН
    df['B'] = df['B'].apply(normalize_inn)

    # Выводим примеры обработанных данных
    print("Примеры данных после обработки:")
    print(df[['A', 'B']].head())

    # Удаляем строки с пустыми значениями в столбцах A или B
    df_filtered = df.dropna(subset=['A', 'B'])
    print(f"Размер датафрейма после удаления пустых строк: {df_filtered.shape}")

    # Создаем список пар (наименование, ИНН)
    company_data = list(zip(df_filtered['A'], df_filtered['B']))
    print(f"Количество компаний для обработки: {len(company_data)}")

    # Выводим список компаний
    print("Список компаний для обработки:")
    for i, (name, inn) in enumerate(company_data, 1):
        print(f"{i}. {name} (ИНН: {inn})")

except Exception as e:
    print(f"Ошибка при чтении Excel файла: {e}")
    print("Убедитесь, что файл имеет формат .xlsx и содержит столбцы с наименованиями и ИНН")
    exit(1)

# Спрашиваем пользователя, хочет ли он продолжить
confirm = input(f"Найдено {len(company_data)} компаний для обработки. Продолжить? (да/нет): ")
if confirm.lower() not in ['да', 'y', 'yes', 'д']:
    print("Операция отменена пользователем.")
    exit(0)

# Инициализация браузера
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)  # Ожидание до 10 секунд
download_folder = get_downloads_folder()
print(f"Файлы будут сохраняться в: {download_folder}")

# Обрабатываем каждую пару (наименование, ИНН) из Excel
for name, inn in company_data:
    try:
        print(f"Обработка: {name} (ИНН: {inn})")

        # Открываем страницу заново для каждого ИНН
        browser.get("https://egrul.nalog.ru/index.html")
        assert "Предоставление" in browser.title

        # Ждем появления поля поиска
        search_box = wait.until(EC.presence_of_element_located((By.ID, "query")))
        search_box.clear()  # Очищаем поле, если в нем есть текст
        search_box.send_keys(inn)  # Теперь inn уже является строкой с правильным форматом
        search_box.send_keys(Keys.RETURN)

        # Ждем появления кнопки "Получить выписку"
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-with-icon.btn-excerpt.op-excerpt")))
        button.click()

        print(f"Запрос выписки для {name} (ИНН: {inn}) отправлен")

        # Даем время для скачивания файла
        time.sleep(5)

        # Переименовываем скачанный файл
        if rename_latest_file(download_folder, name):
            print(f"Выписка для {name} успешно скачана и переименована")
        else:
            print(f"Не удалось переименовать файл для {name}")

    except Exception as e:
        print(f"Ошибка при обработке {name} (ИНН: {inn}): {e}")

# После завершения всех запросов
print("Все запросы выполнены")
browser.quit()