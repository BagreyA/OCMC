#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

using namespace std;

// Порождающий полином G = x^7 + x^6 + x^5 + x^3 + x^2 + x + 1 (в двоичной записи: 1110111)
vector<int> generator = {1, 1, 1, 0, 1, 1, 1};  // Порождающий полином

// Функция для вычисления CRC
vector<int> calculateCRC(const vector<int>& packet, const vector<int>& generator) {
    vector<int> temp(packet);  // Копируем пакет данных
    int generatorSize = generator.size();

    // Добавляем нули в конец пакета для вычисления CRC
    temp.resize(packet.size() + generatorSize - 1, 0);

    // Процесс деления с использованием XOR
    for (int i = 0; i <= temp.size() - generatorSize; ++i) {
        if (temp[i] == 1) {  // XOR только если текущий бит равен 1
            for (int j = 0; j < generatorSize; ++j) {
                temp[i + j] ^= generator[j];
            }
        }
    }

    // Возвращаем остаток (CRC)
    return vector<int>(temp.end() - (generatorSize - 1), temp.end());
}

// Функция для печати вектора (массив битов)
void printVector(const vector<int>& vec) {
    for (int bit : vec) {
        cout << bit;
    }
    cout << endl;
}

int main() {
    srand(time(0));  // Инициализация генератора случайных чисел

    // Пакет данных длиной 250 бит (случайный пример)
    vector<int> packet(250);
    for (int i = 0; i < 250; ++i) {
        packet[i] = rand() % 2;  // Заполняем случайными 0 и 1
    }

    // Вычисление CRC для исходного пакета
    vector<int> crc = calculateCRC(packet, generator);
    cout << "CRC для исходного пакета: ";
    printVector(crc);

    // Добавляем CRC к пакету для передачи
    vector<int> transmittedPacket = packet;
    transmittedPacket.insert(transmittedPacket.end(), crc.begin(), crc.end());

    int mode;
    cout << "Выберите режим работы:" << endl;
    cout << "1 - Без искажения" << endl;
    cout << "2 - С искажением" << endl;
    cout << "Введите номер режима: ";
    cin >> mode;

    // Переменные для подсчета обнаруженных и необнаруженных ошибок
    int errorsDetected = 0;
    int errorsNotDetected = 0;
    int totalBits = transmittedPacket.size();

    // Цикл для искажения по одному биту за раз
    for (int i = 0; i < totalBits; ++i) {
        // Копируем пакет с CRC для искажения одного бита
        vector<int> testPacket = transmittedPacket;

        // В зависимости от выбранного режима
        if (mode == 1) {
            // Без искажения - оставляем пакет как есть
        } else if (mode == 2) {
            // С искажением: инвертируем бит на позиции i
            testPacket[i] = 1 - testPacket[i];
            cout << "Пакет с искажением: ";
            printVector(testPacket);  // Выводим пакет с измененным битом
        }

        // Проверяем искаженный пакет на приемной стороне
        vector<int> remainder = calculateCRC(testPacket, generator);

        // Если остаток не равен нулю, значит ошибка обнаружена
        bool errorDetected = any_of(remainder.begin(), remainder.end(), [](int bit) { return bit != 0; });

        if (errorDetected) {
            errorsDetected++;
        } else {
            errorsNotDetected++;
        }
    }

    // Вывод результатов
    cout << "Обнаружено ошибок: " << errorsDetected << endl;
    cout << "Не обнаружено ошибок: " << errorsNotDetected << endl;

    return 0;
}
