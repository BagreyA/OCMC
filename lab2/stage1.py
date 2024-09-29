import numpy as np
import matplotlib.pyplot as plt
import math

# Константы
c = 3e8  # Скорость света, м/с
f_MHz = 1800  # Частота сигнала в МГц для модели Окумура-Хата и Walfish-Ikegami
f_GHz = f_MHz / 1000 
wavelength = c / (f_MHz * 1e6) 
h_BS = 50  # Высота антенны базовой станции, м
h_MS = 3  # Высота антенны мобильного устройства, м
w = 20  # Средняя ширина улицы, м
b = 30  # Среднее расстояние между зданиями, м
distance_km = np.linspace(0.01, 20, 1000)  # Расстояние в км
distance_m = distance_km * 1000

# Модель FSPM (Free Space Propagation Model) в дБ
def PL_fspm(distance_m, f_MHz):
    return 20 * np.log10((4 * np.pi * distance_m * f_MHz * 1e6) / c)
# Модель UMiNLOS (Urban Micro Non-Line-of-Sight) в дБ
def PL_umi_nlos(distance_m, f_GHz):
    return 26 * np.log10(f_GHz) + 22.7 + 36.7 * np.log10(distance_m)
# Модель Окумура-Хата для городов в дБ (обычный город)
def PL_okumura_hata(distance_km, f_MHz, h_BS, h_MS):
    A = 46.3  # Для частоты 1500-2000 МГц
    B = 33.9
    a_hms = 3.2 * (np.log10(11.75 * h_MS))**2 - 4.97
    s = np.where(distance_km >= 1,
                  44.9 - 6.55 * np.log10(f_MHz),
                  (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(h_BS)) * (1 / np.log10(50)))
    L_clutter = 0 
    PL = A + B * np.log10(f_MHz) - 13.82 * np.log10(h_BS) - a_hms + s * np.log10(distance_km) + L_clutter
    return PL
# Модель COST231-Hata для плотной городской застройки (Dense Urban)
def PL_cost231_hata_dense_urban(distance_km, f_MHz, h_BS, h_MS):
    A = 46.3
    B = 33.9
    a_hms = 3.2 * (np.log10(11.75 * h_MS))**2 - 4.97
    s = np.where(distance_km >= 1,
                  44.9 - 6.55 * np.log10(f_MHz),
                  (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(h_BS)) * (1 / np.log10(50)))
    L_clutter = 3 
    PL = A + B * np.log10(f_MHz) - 13.82 * np.log10(h_BS) - a_hms + s * np.log10(distance_km) + L_clutter
    return PL
# Модель Walfish Ikegami
class WalfishIkegamiModel:
    def __init__(self, f, h_bs, h_ms, w, b):
        self.f = f
        self.h_bs = h_bs
        self.h_ms = h_ms
        self.w = w
        self.b = b

    def calculate_los_losses(self, d):
        return 42.6 + 20 * math.log10(self.f) + 26 * math.log10(d)
    def calculate_non_los_losses(self, d):
        L0 = 32.44 + 20 * math.log10(self.f) + 20 * math.log10(d)
        L1, L2 = self.calculate_non_los_L1_L2(d)
        return L0 + L1 + L2 if L1 + L2 > 0 else L0
    def calculate_non_los_L1_L2(self, d):
        delta_h = self.h_bs - self.h_ms
        phi = 30
        L11 = -18 * math.log10(1 + self.h_bs - delta_h) if self.h_bs > delta_h else 0
        ka = self.calculate_ka(delta_h)
        kd = self.calculate_kd(delta_h)
        kf = -4 + 0.7 * (self.f / 925 - 1)
        L1 = L11 + ka + kd * math.log10(d) + kf * math.log10(self.f) - 9 * math.log10(self.b)
        L2 = self.calculate_L2(phi, delta_h)
        return L1, L2

    def calculate_L2(self, phi, delta_h):
        if phi < 35:
            return -16.9 - 10 * np.log10(self.w) + 10 * np.log10(self.f) + 20 * np.log10(delta_h)
        elif 35 <= phi < 55:
            return -16.9 - 10 * np.log10(self.w) + 10 * np.log10(self.f) + 20 * np.log10(delta_h) - 10 + 0.354 * phi
        return -16.9 - 10 * np.log10(self.w) + 10 * np.log10(self.f) + 20 * np.log10(delta_h) + 4.0 - 0.114 * phi
    def calculate_ka(self, delta_h):
        if self.h_bs > delta_h:
            return 54
        return 54 - 0.8 * (self.h_bs - delta_h)
    def calculate_kd(self, delta_h):
        if self.h_bs > delta_h:
            return 18
        return 18 - 15 * (self.h_bs - delta_h) / delta_h
    def calculate_losses(self, d):
        return self.calculate_los_losses(d) if d <= 0.5 else self.calculate_non_los_losses(d)

walfish_ikegami_model = WalfishIkegamiModel(f_MHz, h_BS, h_MS, w, b)

PL_fspm_values = PL_fspm(distance_m, f_MHz)
PL_umi_nlos_values = PL_umi_nlos(distance_m, f_GHz)
PL_okumura_hata_values = PL_okumura_hata(distance_km, f_MHz, h_BS, h_MS)
PL_cost231_hata_dense_values = PL_cost231_hata_dense_urban(distance_km, f_MHz, h_BS, h_MS)
PL_walfish_values = [walfish_ikegami_model.calculate_losses(d) for d in distance_km]

plt.figure(figsize=(10, 6))
plt.plot(distance_km, PL_fspm_values, label='FSPM (Свободное пространство)', color='blue')
plt.plot(distance_km, PL_umi_nlos_values, label='UMiNLOS (Городская застройка)', color='green')
plt.plot(distance_km, PL_okumura_hata_values, label='COST231-Hata (Города)', color='red')
plt.plot(distance_km, PL_cost231_hata_dense_values, label='COST231-Hata (Плотная застройка)', color='brown', linestyle='--')
plt.plot(distance_km, PL_walfish_values, label='Walfish-Ikegami', color='orange')

plt.title('Зависимость величины потерь радиосигнала от расстояния')
plt.xlabel('Расстояние между приемником и передатчиком (км)')
plt.ylabel('Потери сигнала (дБ)')
plt.grid(True)
plt.legend()
plt.xlim(0, 20)
plt.ylim(0, 250)
plt.show()
