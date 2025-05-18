import pandas as pd

# Загружаем набор данных из CSV-файла в DataFrame
# Замените 'ваш_файл.csv' на реальное имя вашего CSV-файла
df = pd.read_csv('dataset_stats.csv')

# Выводим первые 5 строк данных для представления о структуре
print("Первые 5 строк данных:")
print(df.head())

# Выводим информацию о данных с помощью .info()
print("\nИнформация о данных:")
print(df.info())

# Выводим статистическое описание с помощью .describe()
print("\nСтатистическое описание:")
print(df.describe())

df1 = pd.read_csv('dz.csv', encoding='utf-8')
# Группируем данные по городу и вычисляем среднюю зарплату
avg_salary_by_city = df1.groupby('City')['Salary'].mean()

# Выводим результат
print("\nСредняя зарплата по городам:")
print(avg_salary_by_city)
