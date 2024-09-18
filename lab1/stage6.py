import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Считываем файл
Fs, y = wavfile.read('baia-232.wav')

# Применяем БПФ
L = len(y)
Y = np.fft.fft(y)
P2 = np.abs(Y / L)
P1 = P2[:L//2+1]
P1[1:-1] = 2 * P1[1:-1]

# Вектор частот
f = Fs * np.arange(0, (L/2)+1) / L

# Строим график
plt.plot(f, P1)
plt.title('Односторонний спектр аудиофайла')
plt.xlabel('Частота (Гц)')
plt.ylabel('|P1(f)|')
plt.xlim(50, 1000)  # Например, ограничим до 500 Гц
plt.grid()
plt.show()
