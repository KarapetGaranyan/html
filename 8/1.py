import numpy as np
import matplotlib.pyplot as plt

# Задаем параметры нормального распределения
mean = 0       # Среднее значение
std_dev = 1    # Стандартное отклонение
num_samples = 1000  # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Создаем гистограмму
plt.figure(figsize=(10, 6))  # Задаем размер графика

# Строим гистограмму
plt.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')

# Добавляем теоретическую кривую нормального распределения
x = np.linspace(min(data), max(data), 100)
y = num_samples / 30 * np.exp(-0.5 * ((x - mean) / std_dev) ** 2) / (std_dev * np.sqrt(2 * np.pi))
plt.plot(x, y, 'r--', linewidth=2)

# Добавляем заголовок и подписи осей
plt.title('Гистограмма нормально распределенных данных', fontsize=14)
plt.xlabel('Значение', fontsize=12)
plt.ylabel('Частота', fontsize=12)

# Добавляем информацию о параметрах распределения
plt.text(0.02, 0.95, f'Среднее = {mean}\nСтд. откл. = {std_dev}\nРазмер выборки = {num_samples}',
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

# Добавляем сетку для лучшей читаемости
plt.grid(True, linestyle='--', alpha=0.7)

# Вычисляем и показываем фактическое среднее и стандартное отклонение
actual_mean = np.mean(data)
actual_std = np.std(data)
plt.text(0.02, 0.80, f'Фактическое среднее = {actual_mean:.4f}\nФактическое стд. откл. = {actual_std:.4f}',
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

# Устанавливаем красивые пределы по осям
plt.xlim(mean - 4*std_dev, mean + 4*std_dev)

plt.tight_layout()  # Автоматически настраиваем макет для красивого отображения
plt.show()