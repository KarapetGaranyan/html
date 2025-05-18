import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt


driver = webdriver.Chrome()
url = "https://www.divan.ru/category/divany-i-kresla"
driver.get(url)
time.sleep(3)

divans = driver.find_elements(By.CSS_SELECTOR, 'div.LlPhw')

parsed_data = []

for divan in divans:
    try:
        price = divan.find_element(By.CSS_SELECTOR, 'div.q5Uds span').text
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    parsed_data.append([price])

driver.quit()

with open("prices.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')  # Используем точку с запятой как разделитель
    writer.writerow(['Цена'])  # Заголовок столбца - 'Цена'
    writer.writerows(parsed_data)

# Удаляем "руб." и преобразуем в число
def clean_price(price):
    # Добавляем обработку ошибок
    try:
        # Удаляем все нечисловые символы кроме цифр
        return int(price.replace('руб.', '').replace(' ', '').replace('₽', '').strip())
    except ValueError as e:
        print(f"Ошибка при преобразовании цены '{price}': {e}")
        return 0  # Возвращаем 0 или другое значение по умолчанию в случае ошибки

# Чтение данных из исходного CSV файла и их обработка
input_file = 'prices.csv'
output_file = 'cleaned_prices.csv'

with open(input_file, mode='r', encoding='utf-8-sig') as infile, open(output_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
    reader = csv.reader(infile, delimiter=';')  # Указываем правильный разделитель
    writer = csv.writer(outfile, delimiter=';')  # Используем тот же разделитель для выходного файла

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)  # Сохраняем тот же заголовок

    # Обрабатываем и записываем данные строк
    for row in reader:
        if row:  # Проверяем, что строка не пустая
            clean_row = [clean_price(row[0])]
            writer.writerow(clean_row)

print(f"Обработанные данные сохранены в файл {output_file}")

# Загрузка данных из CSV-файла
file_path = 'cleaned_prices.csv'
data = pd.read_csv(file_path, delimiter=';')  # Не забываем указать разделитель!

# Используем правильное название столбца - 'Цена' вместо 'Price'
prices = data['Цена']  # Исправлено здесь!

# Построение гистограммы
plt.figure(figsize=(10, 6))  # Устанавливаем размер графика
plt.hist(prices, bins=10, edgecolor='black', color='skyblue', alpha=0.7)

# Добавление статистической информации
mean_price = prices.mean()
median_price = prices.median()

# Добавляем вертикальные линии для среднего и медианы
plt.axvline(mean_price, color='red', linestyle='--', linewidth=2,
            label=f'Средняя цена: {mean_price:.2f} руб.')
plt.axvline(median_price, color='green', linestyle='-.', linewidth=2,
            label=f'Медианная цена: {median_price:.2f} руб.')

# Добавление заголовка и меток осей
plt.title('Гистограмма цен на диваны', fontsize=16)
plt.xlabel('Цена (руб.)', fontsize=14)
plt.ylabel('Количество товаров', fontsize=14)

# Добавляем сетку для лучшей читаемости
plt.grid(alpha=0.3)

# Добавляем легенду
plt.legend()

# Добавляем текстовую информацию о статистике
stats_text = f"Количество товаров: {len(prices)}\n" \
             f"Средняя цена: {mean_price:.2f} руб.\n" \
             f"Медианная цена: {median_price:.2f} руб.\n" \
             f"Мин. цена: {prices.min()} руб.\n" \
             f"Макс. цена: {prices.max()} руб."

plt.figtext(0.15, 0.8, stats_text, bbox=dict(facecolor='white', alpha=0.8), fontsize=12)

# Сохраняем гистограмму в файл
plt.savefig('divan_prices_histogram.png')

# Показать гистограмму
plt.tight_layout()  # Автоматическая настройка макета
plt.show()

print("Анализ данных завершен. Гистограмма сохранена в файл 'divan_prices_histogram.png'")