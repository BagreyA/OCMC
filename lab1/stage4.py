import numpy as np

# Параметры сигнала
f = 6           # Частота в Гц
A = 4           # Амплитуда
phi = np.pi / 3 # Фаза

# Параметры дискретизации
fs = 12
t_duration = 1 
N = int(fs * t_duration)

# Генерация временных точек и оцифровка сигнала
t_samples = np.linspace(0, t_duration, N, endpoint=False)
y_samples = A * np.sin(2 * np.pi * f * t_samples + phi)

# Выполнение прямого дискретного преобразования Фурье
Y = np.fft.fft(y_samples)

# Оценка ширины спектра
frequencies = np.fft.fftfreq(N, d=1/fs)

# Определяем ширину спектра - максимальная частота
max_frequency = np.max(np.abs(Y))
Frequency_bin_width = frequencies[1] - frequencies[0]

# Объем памяти, занимаемый массивом
memory_usage = y_samples.nbytes
memory_usage_kb = memory_usage / 1024 

# Вывод результатов
print("Дискретное преобразование Фурье (амплитуда):", np.abs(Y))
print("Ширина спектра (максимальная частота):", max_frequency)
print("Объем памяти, занятый массивом y_samples:", memory_usage_kb, "КБ")
