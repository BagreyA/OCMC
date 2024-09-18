import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
f = 6
A = 4
phi = np.pi / 3

# Параметры дискретизации
fs = 12
t_duration = 1
N = int(fs * t_duration) 

# Генерация временных точек с частотой дискретизации 12 Гц
t_samples = np.linspace(0, t_duration, N, endpoint=False)  
y_samples = A * np.sin(2 * np.pi * f * t_samples + phi)

# Сохранение в массиве (y_samples уже является массивом с оцифрованными значениями)
print("Временные точки (с):", t_samples)
print("Оцифрованные значения сигнала:", y_samples)
plt.figure(figsize=(10, 5))
plt.plot(t_samples, y_samples, marker='o', linestyle='-')
plt.title('Оцифрованный сигнал (6 Гц)')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid()
plt.show()

