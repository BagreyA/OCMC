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

distance_km = np.linspace(0.01, 20, 1000)

def PL_cost231_hata_dense_urban(distance_km, f_MHz=1800, h_BS=50, h_MS=1.5):
    A = 46.3
    B = 33.9
    a_hms = 3.2 * (np.log10(11.75 * h_MS))**2 - 4.97
    
    s = np.where(distance_km >= 1,
                  44.9 - 6.55 * np.log10(f_MHz),
                  (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(h_BS)) * (1 / np.log10(50)))

    L_clutter = 3 #(или 0) 
    PL = A + B * np.log10(f_MHz) - 13.82 * np.log10(h_BS) - a_hms + s * np.log10(distance_km) + L_clutter
    return PL

PL = PL_cost231_hata_dense_urban(distance_km)  # Используем обновленную модель COST 231 Hata

plt.figure(figsize=(10, 6))
plt.plot(distance_km, PL, label='COST 231 Hata', color='blue')

plt.axhline(y=MAPL_UL, color='green', linestyle='--', label='MAPL_UL')
plt.axhline(y=MAPL_DL, color='red', linestyle='--', label='MAPL_DL')

d_UL_ind = np.where(PL <= MAPL_UL)[0]
d_DL_ind = np.where(PL <= MAPL_DL)[0]

d_UL = distance_km[d_UL_ind[-1]] if d_UL_ind.size > 0 else None
d_DL = distance_km[d_DL_ind[-1]] if d_DL_ind.size > 0 else None

if d_UL is not None:
    plt.axvline(x=d_UL, color='green')
if d_DL is not None:
    plt.axvline(x=d_DL, color='red')

if d_UL is not None:
    plt.text(d_UL + 0.1, MAPL_UL + 5, f'd_UL = {d_UL:.2f} км', color='green')
if d_DL is not None:
    plt.text(d_DL + 0.1, MAPL_DL + 5, f'd_DL = {d_DL:.2f} км', color='red')

d_min = min(d_UL, d_DL)  
number_of_sectors = 3 

if number_of_sectors == 6:
    area_per_bs = 2.6 * (d_UL ** 2)
elif number_of_sectors == 2:
    area_per_bs = 1.73 * (d_UL ** 2)
elif number_of_sectors == 3:
    area_per_bs = 1.95 * (d_UL ** 2)
else:
    area_per_bs = 0 

total_area = 100  
area_business_centers = 4 

number_bs_total = total_area / area_per_bs
number_bs_business_centers = area_business_centers / area_per_bs

results = [
    ['Площадь одной БС (кв.км)', f'{area_per_bs:.2f}'],
    ['Необходимые БС (100 кв.км)', f'{np.ceil(number_bs_total):.0f}'],
    ['Необходимые БС (4 кв.км)', f'{np.ceil(number_bs_business_centers):.0f}']
]

table = plt.table(cellText=results, colLabels=['Параметр', 'Значение'], loc='right', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1) 

plt.title('Зависимость потерь радиосигнала от расстояния')
plt.xlabel('Расстояние (км), L_clutter = 0')
plt.ylabel('Потери (дБ)')
plt.grid(True)
plt.legend()
plt.xlim(0, 10)
plt.ylim(0, 250)
plt.show()
