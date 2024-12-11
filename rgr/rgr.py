import numpy as np
import matplotlib.pyplot as plt

def encode_to_bits(input_str):
    packet = []
    for char in input_str:
        # Преобразование символа в биты
        bits = [int(bit) for bit in format(ord(char), '08b')]
        packet.extend(bits)  # Добавляем биты в общий список
    return packet

def decode_from_bits(packet):
    if len(packet) % 8 != 0:
        raise ValueError("Длина пакета должна быть кратной 8 для корректного декодирования.")

    output = []
    # Преобразуем каждые 8 бит в символ
    for i in range(0, len(packet), 8):
        bits = packet[i:i+8]
        byte = int(''.join(str(b) for b in bits), 2)  # Преобразуем массив бит в десятичное значение
        output.append(chr(byte))  # Преобразуем байт в символ и добавляем к результату
    
    return ''.join(output)

def disp_bits(bits):
    for i in range(len(bits)):
        print(bits[i], end='')
        if (i + 1) % 8 == 0:
            print(' ', end='')  # Пробел после каждых 8 бит
    print()

def calculate_crc(packet, generator):
    packet = np.array(packet)
    temp = np.concatenate([packet, np.zeros(len(generator) - 1, dtype=int)])

    crc_length = 0  # Счетчик длины CRC
    end_index = -1  # Индекс, где заканчивается CRC
    generator_length = len(generator)

    for i in range(len(packet)):
        if temp[i] == 1:
            # Выполняем XOR с порождающим полиномом
            temp[i:i + generator_length] = np.bitwise_xor(temp[i:i + generator_length], generator)
        
        crc_length += 1

        # Проверяем, состоит ли остаток после текущей позиции только из нулей
        if np.all(temp[i+1:] == 0):
            end_index = i + generator_length - 1
            break

    # Извлекаем CRC
    crc = temp[-(generator_length - 1):]
    return crc, crc_length, end_index

def check_packet(packet_with_crc, generator):
    remainder, crc_length, end_index = calculate_crc(packet_with_crc, generator)
    is_valid = np.all(remainder == 0)  # Проверяем, что остаток равен нулю
    return is_valid, crc_length, end_index

def generate_sequence_gold(x, y, length_sequence):
    gold_sequence = np.zeros(length_sequence, dtype=int)
    for i in range(length_sequence):
        x, shift_bit_x = shift_sequence(x, 2, 4)
        y, shift_bit_y = shift_sequence(y, 2, 4)
        gold_sequence[i] = shift_bit_x ^ shift_bit_y  # XOR двух последовательностей
    return gold_sequence

def shift_sequence(seq, element_1, element_2):
    shift_bit = seq[element_1] ^ seq[element_2]  # XOR элементов
    last_bit = seq[-1]
    seq = np.concatenate(([shift_bit], seq[:-1]))  # Сдвиг влево
    return seq, last_bit

def repeat_elements(input_vector, N):
    output_vector = np.array([])
    for elem in input_vector:
        output_vector = np.concatenate((output_vector, np.repeat(elem, N)))
    return output_vector

def insert_array_at_position(target_vector, array_to_insert, position):
    if position + len(array_to_insert) - 1 > len(target_vector):
        raise ValueError("Размер массива для вставки превышает размер целевого вектора.")
    
    target_vector[position:position+len(array_to_insert)] = array_to_insert
    return target_vector

# Генерация нормального шума
def generate_noise(size, mu, sigma):
    noise = mu + sigma * np.random.randn(size)  
    return noise

def find_sync_sequence_start(array_with_hastle, gold_sequence_double, N, L, M, G):
    sync_start_index = -1  # По умолчанию синхроимпульс не найден
    G_N = G * N  # Длина синхронизирующей последовательности
    
    if len(array_with_hastle) < G_N:
        print('Длина массива слишком мала для поиска синхронизирующей последовательности.')
        return sync_start_index, []
    
    # Инициализация массива для хранения корреляций
    correlations = np.zeros(len(array_with_hastle) - G_N + 1)
    
    # Проход по массиву для поиска синхронизирующей последовательности
    for i in range(len(array_with_hastle) - G_N + 1):
        # Извлекаем подмассив длиной G * N начиная с позиции i
        synchro_sequence = array_with_hastle[i:i + G_N]
        # Вычисляем корреляцию между подмассивом и эталонной последовательностью
        result = np.corrcoef(synchro_sequence, gold_sequence_double)[0, 1]
        
        correlations[i] = result
        
        # Проверяем, если корреляция близка к 1 (синхроимпульс найден)
        if abs(result) >= 0.76:
            print(f'Найден вход в синхроимпульс на индексе: {i}')
            sync_start_index = i
            break
    
    if sync_start_index == -1:
        print('Синхроимпульс не найден.')
    
    return sync_start_index, correlations


def decode_signal(signal, N):
    # Порог для интерпретации
    P = 0.6  
    decoded_bits = []

    signal_length = len(signal)

    # Обработка сигналов группами длиной N
    for i in range(0, signal_length - N + 1, N):
        segment = signal[i:i + N]  # Извлекаем сегмент длиной N
        average = np.mean(segment)

        if average >= P:
            decoded_bits.append(1)  # Если среднее выше порога, добавляем 1
        else:
            decoded_bits.append(0)  # Иначе добавляем 0
    
    return decoded_bits

# Ввод фамилии и имени в одну строку
full_name = input('Введите фамилию и имя (через пробел): ')

surname, name = full_name.split()

packet = encode_to_bits(full_name)
print('Битовое представление фамилии и имени:')
disp_bits(packet)

plt.figure()
plt.plot(packet, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Визуализация сигнала', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(packet)])
plt.ylim([min(packet) - 0.5, max(packet) + 0.5])
plt.show()

g_sequence = [1, 1, 1, 0, 1, 1, 1, 1]
# Генерация CRC для пакета
crc, crc_length, end_index = calculate_crc(packet, g_sequence)
crc = np.array(crc).flatten()
packet_with_crc = np.concatenate([packet, crc])
print('CRC:')
print(crc)
# Вывод объединенного пакета
print('Пакет с CRC:')
disp_bits(packet_with_crc)

# Генерация последовательности Голда
length_sequence_gold = 31
x = [0, 0, 1, 0, 0]
y = [0, 1, 1, 0, 1]
gold_sequence = generate_sequence_gold(x, y, length_sequence_gold)

L = len(packet)
M = len(crc)
G = len(gold_sequence)
N = 6  # Частота дискретизации
N1 = N // 2
N2 = N * 2
ar_data = np.tile(np.concatenate([gold_sequence, packet_with_crc]), 1)
ar_data_1 = np.tile(np.concatenate([gold_sequence, packet_with_crc]), 1)
ar_data_2 = np.tile(np.concatenate([gold_sequence, packet_with_crc]), 1)

# частота дискретизации
ar_out = np.zeros(2 * N * (L + M + G))
# уменьшенная частота дискретизации в 2 раза
ar_out_1 = np.zeros(2 * N1 * (L + M + G))
# увеличенная частота дискретизации в 2 раза
ar_out_2 = np.zeros(2 * N2 * (L + M + G))

plt.figure()
plt.plot(ar_data, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал: Голд, Данные и CRC', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_data)])
plt.ylim([min(ar_data) - 0.5, max(ar_data) + 0.5])
plt.show()

# Повторение элементов для изменения частоты дискретизации
ar_data = repeat_elements(ar_data, N)
ar_data_1 = repeat_elements(ar_data_1, N1)
ar_data_2 = repeat_elements(ar_data_2, N2)

plt.figure()
plt.subplot(3, 1, 1)
plt.plot(ar_data, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал: Частота * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_data)])
plt.ylim([min(ar_data) - 0.5, max(ar_data) + 0.5])

plt.subplot(3, 1, 2)
plt.plot(ar_data_1, color='red', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал: (Частота/2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_data_1)])
plt.ylim([min(ar_data_1) - 0.5, max(ar_data_1) + 0.5])

plt.subplot(3, 1, 3)
plt.plot(ar_data_2, color='orange', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал: (Частота * 2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_data_2)])
plt.ylim([min(ar_data_2) - 0.5, max(ar_data_2) + 0.5])
plt.tight_layout()
plt.show()

flag = True
while flag:
    position = int(input(f'Введите позицию вставки (0 <= позиция <= {N * (L + M + G)}): '))
    if 0 <= position <= N * (L + M + G):
        print('Значение лежит в диапазоне')
        flag = False
    else:
        print('Значение вне диапазона')

# Вставка данных
ar_out = insert_array_at_position(ar_out, ar_data, position)
ar_out_1 = insert_array_at_position(ar_out_1, ar_data_1, position)
ar_out_2 = insert_array_at_position(ar_out_2, ar_data_2, position)

plt.figure()
plt.subplot(3, 1, 1)
plt.plot(ar_out, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал после вставки данных: Частота * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_out)])
plt.ylim([min(ar_out) - 0.5, max(ar_out) + 0.5])

plt.subplot(3, 1, 2)
plt.plot(ar_out_1, color='red', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал после вставки данных: (Частота/2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_out_1)])
plt.ylim([min(ar_out_1) - 0.5, max(ar_out_1) + 0.5])

plt.subplot(3, 1, 3)
plt.plot(ar_out_2, color='orange', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал после вставки данных: (Частота * 2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(ar_out_2)])
plt.ylim([min(ar_out_2) - 0.5, max(ar_out_2) + 0.5])
plt.tight_layout()
plt.show()

sigma = float(input('Введите стандартное отклонение шума: '))

# Генерация шума
ar_with_hastle = generate_noise(2 * N * (L + M + G), 0, sigma)
ar_with_hastle_1 = generate_noise(2 * N1 * (L + M + G), 0, sigma)
ar_with_hastle_2 = generate_noise(2 * N2 * (L + M + G), 0, sigma)

ar_out = ar_out.astype(float)
ar_out_1 = ar_out_1.astype(float)
ar_out_2 = ar_out_2.astype(float)

# Добавление шума
result = ar_out + ar_with_hastle
result_1 = ar_out_1 + ar_with_hastle_1
result_2 = ar_out_2 + ar_with_hastle_2

plt.figure()
plt.subplot(3, 1, 1)
plt.plot(result, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал с шумом: Частота * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(result)])
plt.ylim([min(result) - 0.5, max(result) + 0.5])

plt.subplot(3, 1, 2)
plt.plot(result_1, color='red', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал с шумом: (Частота/2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(result_1)])
plt.ylim([min(result_1) - 0.5, max(result_1) + 0.5])

plt.subplot(3, 1, 3)
plt.plot(result_2, color='orange', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сигнал с шумом: (Частота * 2) * (Голд, Данные и CRC)', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(result_2)])
plt.ylim([min(result_2) - 0.5, max(result_2) + 0.5])

plt.tight_layout()
plt.show()

# Находим начало синхропоследовательности
gold_sequence_double = np.repeat(gold_sequence, N)
sync_index, correlation = find_sync_sequence_start(result, gold_sequence_double, N, L, M, G)

plt.figure()
plt.plot(correlation, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Визуализация сигнала с помехами', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(correlation)])
plt.ylim([min(correlation) - 0.5, max(correlation) + 0.5])
plt.show()

print(sync_index)

# Обрезаем до синхронизации
signal_out = result[sync_index:]

plt.figure()
plt.plot(signal_out, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сокращение до синхронизации', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(signal_out)])
plt.ylim([min(signal_out) - 0.5, max(signal_out) + 0.5])
plt.show()

# Декодирование сигнала
bits_sequence = decode_signal(signal_out, N)

plt.figure()
plt.plot(bits_sequence, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Декодирование битов', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(bits_sequence)])
plt.ylim([min(bits_sequence) - 0.5, max(bits_sequence) + 0.5])
plt.show()

bit_seq_WN = bits_sequence

plt.figure()
plt.plot(bit_seq_WN, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сокращение до последовательности Голда', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(bit_seq_WN)])
plt.ylim([min(bit_seq_WN) - 0.5, max(bit_seq_WN) + 0.5])
plt.show()

bit_seq_WNG = bit_seq_WN[G:]

plt.figure()
plt.plot(bit_seq_WNG, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сокращение последовательности Голда', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(bit_seq_WNG)])
plt.ylim([min(bit_seq_WNG) - 0.5, max(bit_seq_WNG) + 0.5])
plt.show()

# Проверка на приемной стороне
is_valid, crc_length, end_index = check_packet(packet_with_crc, g_sequence)
print(crc_length)
print(end_index)

if is_valid:
    print('Ошибок не обнаружено в принятом пакете.')
else:
    print('Ошибка обнаружена в принятом пакете.')

bit_seq_WNGM = bit_seq_WNG[:crc_length]

plt.figure()
plt.plot(bit_seq_WNGM, color='green', linewidth=2)
plt.xlabel('Время', fontsize=12, fontweight='bold')
plt.ylabel('Сигнал', fontsize=12, fontweight='bold')
plt.title('Сокращение CRC + шум', fontsize=14, fontweight='bold')
plt.grid(True)
plt.xlim([0, len(bit_seq_WNGM)])
plt.ylim([min(bit_seq_WNGM) - 0.5, max(bit_seq_WNGM) + 0.5])
plt.show()

# Декодирование слова
slovo = decode_from_bits(bit_seq_WNGM)
print(slovo)