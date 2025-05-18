import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://www.divan.ru/category/svet"
driver.get(url)
time.sleep(3)

divans = driver.find_elements(By.CSS_SELECTOR, 'div.LlPhw')

parsed_data = []

for divan in divans:
    try:
        name = divan.find_element(By.CSS_SELECTOR, 'div.lsooF span').text
        price = divan.find_element(By.CSS_SELECTOR, 'div.q5Uds span').text
        url = divan.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(url)
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    parsed_data.append([name, price, url])

driver.quit()

with open("divan.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')  # Используем точку с запятой как разделитель
    writer.writerow(['Название', 'Цена', 'Ссылка'])
    writer.writerows(parsed_data)