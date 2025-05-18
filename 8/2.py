import numpy as np
import matplotlib.pyplot as plt

# Устанавливаем seed для воспроизводимости результатов
np.random.seed(42)

# Генерируем первый массив из 5 случайных чисел в диапазоне [0, 1)
random_array1 = np.random.rand(5)
print("Первый массив:", random_array1)

# Генерируем второй массив из 5 случайных чисел в диапазоне [0, 1)
random_array2 = np.random.rand(5)
print("Второй массив:", random_array2)

# Создаем фигуру с графиком
plt.figure(figsize=(10, 6))

# Строим диаграмму рассеяния
plt.scatter(random_array1, random_array2, color='blue', marker='o', s=100, alpha=0.7, label='Случайные точки')

# Добавляем подписи к каждой точке
for i in range(len(random_array1)):
    plt.annotate(f'Точка {i+1}',
                 (random_array1[i], random_array2[i]),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')

# Добавляем заголовок и подписи осей
plt.title('Диаграмма рассеяния для двух наборов случайных данных', fontsize=14)
plt.xlabel('Первый набор случайных чисел', fontsize=12)
plt.ylabel('Второй набор случайных чисел', fontsize=12)

# Добавляем легенду
plt.legend()

# Добавляем сетку для лучшей читаемости
plt.grid(True, linestyle='--', alpha=0.7)

# Устанавливаем пределы осей (немного расширяем диапазон [0, 1])
plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)

# Добавляем информацию о данных
plt.text(0.02, 0.98, f'Массив 1: {np.round(random_array1, 3)}\nМассив 2: {np.round(random_array2, 3)}',
         transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

# Настраиваем макет для красивого отображения
plt.tight_layout()

# Показываем график
plt.show()