import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os


def create_fns_report(inn):
    """
    Автоматизация запроса на сайте ФНС России

    Args:
        inn (str): ИНН организации для проверки
    """

    # Настройка Chrome драйвера
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Открываем сайт ФНС...")
        driver.get("https://service.nalog.ru/bi.do")

        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 10)

        # Поиск и выбор первой галочки "Запрос о действующих приостановлениях операций по счетам"
        print("Выбираем тип запроса...")

        # Ждем появления чекбокса и кликаем по нему
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][@value='1']")))
        checkbox.click()

        time.sleep(1)

        # Поиск поля ввода ИНН
        print(f"Вводим ИНН: {inn}")
        inn_field = wait.until(EC.presence_of_element_located((By.NAME, "inn")))
        inn_field.clear()
        inn_field.send_keys(inn)

        # Поиск поля ввода БИК
        print("Вводим БИК: 046015064")
        bik_field = wait.until(EC.presence_of_element_located((By.NAME, "bik")))
        bik_field.clear()
        bik_field.send_keys("046015064")

        time.sleep(1)

        # Поиск и нажатие кнопки отправки запроса
        print("Отправляем запрос...")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
        submit_button.click()

        # Ожидание загрузки результатов
        time.sleep(3)

        # Создание скриншота
        print("Создаем скриншот...")
        screenshot = driver.get_screenshot_as_png()

        # Сохранение скриншота в PDF
        print("Сохраняем в PDF...")
        save_screenshot_as_pdf(screenshot, "ФНС.pdf")

        print("Готово! Файл ФНС.pdf создан.")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

    finally:
        # Закрытие браузера
        driver.quit()


def save_screenshot_as_pdf(screenshot_data, filename):
    """
    Сохранение скриншота в PDF файл

    Args:
        screenshot_data: Данные скриншота в формате PNG
        filename (str): Имя файла для сохранения
    """

    # Открываем изображение из байтов
    image = Image.open(io.BytesIO(screenshot_data))

    # Получаем размеры изображения
    img_width, img_height = image.size

    # Создаем PDF
    c = canvas.Canvas(filename, pagesize=A4)

    # Размеры страницы A4 в пунктах
    page_width, page_height = A4

    # Масштабируем изображение под размер страницы
    scale_x = page_width / img_width
    scale_y = page_height / img_height
    scale = min(scale_x, scale_y)

    new_width = img_width * scale
    new_height = img_height * scale

    # Центрируем изображение на странице
    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2

    # Сохраняем временный файл изображения
    temp_image_path = "temp_screenshot.png"
    image.save(temp_image_path)

    # Добавляем изображение в PDF
    c.drawImage(temp_image_path, x, y, width=new_width, height=new_height)
    c.save()

    # Удаляем временный файл
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)


# Основная функция для запуска
def main():
    """
    Основная функция для запуска скрипта
    """

    # Запрос ИНН у пользователя
    inn = input("Введите ИНН для проверки: ")

    # Валидация ИНН (базовая проверка)
    if not inn.isdigit() or len(inn) not in [10, 12]:
        print("Ошибка: ИНН должен содержать только цифры и быть длиной 10 или 12 символов")
        return

    # Запуск автоматизации
    create_fns_report(inn)


if __name__ == "__main__":
    main()