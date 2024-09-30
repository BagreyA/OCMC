import numpy as np 
import matplotlib.pyplot as plt

P_tx_UL = 24  # мощность передатчика UE, дБм
P_tx_DL = 46  # мощность передатчика BS, дБм
I_noise_UL = 6  # уровень шума для UE, дБ
I_noise_DL = 2.4  # уровень шума для BS, дБ
SINR_UL = 4  # требуемое SINR для UL, дБ
SINR_DL = 2  # требуемое SINR для DL, дБ
MAPL_UL = 126.7 
MAPL_DL = 144.1  

distance_km = np.linspace(0.01, 100, 1000)

# Функция для модели COST 231 Hata для плотной городской застройки
def PL_cost231_hata_dense_urban(distance_km, f_MHz=1800, h_BS=50, h_MS=3):
    A = 46.3
    B = 33.9
    a_hms = 3.2 * (np.log10(11.75 * h_MS))**2 - 4.97
    
    s = np.where(distance_km >= 1,
                  44.9 - 6.55 * np.log10(f_MHz),
                  (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(h_BS)) * (1 / np.log10(50)))

    L_clutter = 0  # Затухание сигнала из-за препятствий (например, здания)
    PL = A + B * np.log10(f_MHz) - 13.82 * np.log10(h_BS) - a_hms + s * np.log10(distance_km) + L_clutter
    return PL

# Функция для модели UMiNLOS (улицы городской застройки)
def PL_UMiNLOS(distance_km, f_MHz=1800, h_BS=50, h_MS=3):
    PL = 36.7 * np.log10(distance_km) + 22.7 + 26 * np.log10(f_MHz)
    return PL

# Расчет потерь сигнала на разных расстояниях
PL_Macro = PL_cost231_hata_dense_urban(distance_km)
PL_Micro = PL_UMiNLOS(distance_km)

# Создание графика
plt.figure(figsize=(10, 6))

plt.plot(distance_km, PL_Macro, label='COST 231 Hata (Macrocells)', color='blue')
plt.plot(distance_km, PL_Micro, label='UMiNLOS (Microcells)', color='orange')

# Линии максимально допустимых потерь (MAPL)
plt.axhline(y=MAPL_UL, color='green', linestyle='--', label='MAPL_UL')
plt.axhline(y=MAPL_DL, color='red', linestyle='--', label='MAPL_DL')

# Определение расстояний, где потери соответствуют MAPL
d_MAC_UL_ind = np.where(PL_Macro <= MAPL_UL)[0]
d_MAC_DL_ind = np.where(PL_Macro <= MAPL_DL)[0]
d_MIC_UL_ind = np.where(PL_Micro <= MAPL_UL)[0]
d_MIC_DL_ind = np.where(PL_Micro <= MAPL_DL)[0]

d_MAC_UL = distance_km[d_MAC_UL_ind[-1]] if d_MAC_UL_ind.size > 0 else None
d_MAC_DL = distance_km[d_MAC_DL_ind[-1]] if d_MAC_DL_ind.size > 0 else None
d_MIC_UL = distance_km[d_MIC_UL_ind[-1]] if d_MIC_UL_ind.size > 0 else None
d_MIC_DL = distance_km[d_MIC_DL_ind[-1]] if d_MIC_DL_ind.size > 0 else None

# Рисуем вертикальные линии для расстояний
if d_MAC_UL is not None:
    plt.axvline(x=d_MAC_UL, color='blue', linestyle=':')
if d_MAC_DL is not None:
    plt.axvline(x=d_MAC_DL, color='red', linestyle=':')
if d_MIC_UL is not None:
    plt.axvline(x=d_MIC_UL, color='orange', linestyle=':')
if d_MIC_DL is not None:
    plt.axvline(x=d_MIC_DL, color='orange', linestyle='--')

# Добавление текстовых аннотаций
if d_MAC_UL is not None:
    plt.text(d_MAC_UL + 0.5, MAPL_UL + 5, f'd_MAC_UL = {d_MAC_UL:.2f} км', color='blue')
if d_MAC_DL is not None:
    plt.text(d_MAC_DL + 0.5, MAPL_DL + 5, f'd_MAC_DL = {d_MAC_DL:.2f} км', color='red')
if d_MIC_UL is not None:
    plt.text(d_MIC_UL + 0.5, MAPL_UL + 5, f'd_MIC_UL = {d_MIC_UL:.2f} км', color='orange')
if d_MIC_DL is not None:
    plt.text(d_MIC_DL + 0.5, MAPL_DL + 5, f'd_MIC_DL = {d_MIC_DL:.2f} км', color='orange')

# Подсчёт минимальных расстояний
d_min_macro = min(d_MAC_UL, d_MAC_DL) if d_MAC_UL is not None and d_MAC_DL is not None else None
d_min_micro = min(d_MIC_UL, d_MIC_DL) if d_MIC_UL is not None and d_MIC_DL is not None else None
d_min = min(d_min_macro, d_min_micro) if d_min_macro and d_min_micro else (d_min_macro or d_min_micro)

# Площадь одной базовой станции
area_per_bs_macro = 1.95 * (d_min_macro ** 2) if d_min_macro is not None else 0
area_per_bs_micro = 1.95 * (d_min_micro ** 2) if d_min_micro is not None else 0

# Общая площадь
total_area = 100  # Общая площадь в кв. км
area_business_centers = 4  # Площадь торговых и бизнес-центров в кв. км

# Необходимое количество базовых станций
number_bs_total_macro = total_area / area_per_bs_macro if area_per_bs_macro > 0 else np.inf
number_bs_business_centers_macro = area_business_centers / area_per_bs_macro if area_per_bs_macro > 0 else np.inf
number_bs_total_micro = area_business_centers / area_per_bs_micro if area_per_bs_micro > 0 else np.inf

# Площадь для ячеек
number_of_sectors = 3  # 3 сектора для всех сот
cell_area_macro = area_per_bs_macro / number_of_sectors if area_per_bs_macro > 0 else 0
cell_area_micro = area_per_bs_micro/ number_of_sectors if area_per_bs_macro > 0 else 0

# Формирование таблицы результатов
results = [
    ['Площадь одной соты (кв.км, макро)', f'{cell_area_macro:.2f}'],
    ['Площадь одной БС (кв.км, макро)', f'{area_per_bs_macro:.2f}'],
    ['Необходимые БС (100 кв.км, макро)', f'{np.ceil(number_bs_total_macro):.0f}'],
    ['Необходимые БС (4 кв.км, макро)', f'{np.ceil(number_bs_business_centers_macro):.0f}'],
    ['Площадь одной соты (кв.км, микро)', f'{cell_area_micro:.2f}'],
    ['Площадь одной БС (кв.км, микро)', f'{area_per_bs_micro:.2f}'],
    ['Необходимые БС (4 кв.км, микро)', f'{np.ceil(number_bs_total_micro):.0f}']
]

# Отображение таблицы результатов
table = plt.table(cellText=results, colLabels=['Параметр', 'Значение'], loc='right', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1)

# Настройки графика
plt.title('Зависимость потерь радиосигнала от расстояния (COST 231 Hata и UMiNLOS)')
plt.xlabel('Расстояние (км), L_clutter = 0')
plt.ylabel('Потери (дБ)')
plt.grid(True)
plt.legend()
plt.xlim(0, 20)
plt.ylim(0, 
plt.xlim(0, 10)
plt.ylim(0, 250)
plt.show()
