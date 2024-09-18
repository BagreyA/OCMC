import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
f = 6
A = 4
phi = np.pi / 3

fs = 12
t_duration = 1 
N = int(fs * t_duration)  

# Генерация временных точек и оцифровка сигнала
t_samples = np.linspace(0, t_duration, N, endpoint=False)
y_samples = A * np.sin(2 * np.pi * f * t_samples + phi)

# Восстановление оригинального сигнала с помощью интерполяции
t_fine = np.linspace(0, t_duration, 1000)  
y_fine = A * np.sin(2 * np.pi * f * t_fine + phi)  

# Визуализация
plt.figure(figsize=(12, 6))
plt.plot(t_fine, y_fine, label='Оригинальный сигнал', color='blue')
plt.plot(t_samples, y_samples, 'o-', label='Восстановленный сигнал (отсчеты)', color='orange')
plt.title('Сравнение оригинального и восстановленного сигнала')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid()
plt.xlim(0, t_duration)
plt.ylim(-5, 5)
plt.show()

