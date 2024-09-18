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

# Преобразование Фурье
Y = np.fft.fft(y)
N = len(Y) # Количество точек
Y_magnitude = np.abs(Y) / N
frequencies = np.fft.fftfreq(N, d=0.001) 
# Визуализация спектра
plt.figure()
plt.plot(frequencies[:N // 2], Y_magnitude[:N // 2]) 
plt.title('Спектр сигнала')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.grid()
plt.xlim(0, 20)
plt.show()
