import pandas as pd
import numpy as np

# 1. Самостоятельно создаём DataFrame с данными
# Создаём случайные данные для 10 учеников по 5 предметам
# Оценки от 2 до 5
np.random.seed(42)  # Для воспроизводимости результатов

students = [f"Ученик_{i+1}" for i in range(10)]
subjects = ['Математика', 'Русский', 'Физика', 'История', 'Информатика']

# Генерируем случайные оценки от 2 до 5
data = np.random.randint(2, 6, size=(10, 5))

# Создаём DataFrame
df = pd.DataFrame(data, index=students, columns=subjects)

# 2. Выводим первые несколько строк DataFrame
print("Первые несколько строк DataFrame:")
print(df.head())
print("\n")

# 3. Вычисляем среднюю оценку по каждому предмету
mean_scores = df.mean()
print("Средняя оценка по каждому предмету:")
print(mean_scores)
print("\n")

# 4. Вычисляем медианную оценку по каждому предмету
median_scores = df.median()
print("Медианная оценка по каждому предмету:")
print(median_scores)
print("\n")

# 5. Вычисляем Q1 и Q3 для оценок по математике
Q1_math = df['Математика'].quantile(0.25)
Q3_math = df['Математика'].quantile(0.75)
print(f"Q1 для оценок по математике: {Q1_math}")
print(f"Q3 для оценок по математике: {Q3_math}")
print("\n")

# Расчёт IQR (межквартильный размах)
IQR_math = Q3_math - Q1_math
print(f"IQR для оценок по математике: {IQR_math}")
print("\n")

# 6. Вычисляем стандартное отклонение
std_scores = df.std()
print("Стандартное отклонение по каждому предмету:")
print(std_scores)
print("\n")

# Дополнительная статистика для более полного анализа
print("Полная статистика по всем предметам:")
print(df.describe())
print("\n")

# Визуализация для лучшего понимания (можно раскомментировать при необходимости)
# import matplotlib.pyplot as plt
# import seaborn as sns

# plt.figure(figsize=(12, 6))
#
# # Boxplot для визуализации распределения оценок
# sns.boxplot(data=df)
# plt.title('Распределение оценок по предметам')
# plt.ylabel('Оценки')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()