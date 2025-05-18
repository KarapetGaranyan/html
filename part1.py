import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
time.sleep(3)

vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-info--ieHKDTkezpEj0Gsx')

parsed_data = []

for vacancy in vacancies:
    try:
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_5-0-11')
        title = title_element.text
        link = title_element.get_attribute('href')
        company = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-employer-text"]').text

        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, 'span.magritte-text___pbpft_3-0-33').text
        except:
            salary = "Не указана"

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    parsed_data.append([title, company, salary, link])

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')  # Используем точку с запятой как разделитель
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)