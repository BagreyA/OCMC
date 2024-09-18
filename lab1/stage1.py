import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
f = 6           # Частота в Гц
A = 4           # Амплитуда
phi = np.pi / 3 # Фаза

# Временные параметры
t = np.arange(0, 1, 0.001)

# Генерация сигнала
y = A * np.sin(2 * np.pi * f * t + phi)

plt.figure()
plt.plot(t, y)
plt.title('Непрерывный сигнал y(t) = 4sin(2πft + π/3)')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid()
plt.axis('tight')
plt.show()
