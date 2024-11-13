#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Порождающий полином G = x^7+x^6+x^5+x^3+x^2+x+1
vector<int> generator = {1, 1, 1, 0, 1, 1, 1};
// Функция для вычисления CRC
vector<int> calculateCRC(const vector<int>& packet, const vector<int>& generator) {
    vector<int> temp(packet);
    int generatorSize = generator.size();
    // Добавляем нули в конец пакета для вычисления CRC
    temp.resize(packet.size() + generatorSize - 1, 0);
    cout << "Исходный пакет с добавленными нулями: ";
    for (int bit : temp) cout << bit;
    cout << endl;

    // Процесс деления с использованием XOR
    for (int i = 0; i <= temp.size() - generatorSize; ++i) {
        if (temp[i] == 1) {
            cout << "Шаг " << i + 1 << ": XOR на позиции " << i << endl;
            cout << "До выполнения XOR: ";
            for (int bit : temp) cout << bit;
            cout << endl;
            // XOR с порождающим полиномом
            for (int j = 0; j < generatorSize; ++j) {
                temp[i + j] ^= generator[j];
            }
            cout << "После выполнения XOR: ";
            for (int bit : temp) cout << bit;
            cout << endl;
        }
    }
    // Возвращаем остаток (CRC), последние биты после выполнения XOR
    return vector<int>(temp.end() - (generatorSize - 1), temp.end());
}

void printVector(const vector<int>& vec) {
    for (int bit : vec) {
        cout << bit;
    }
    cout << endl;
}

int main() {
    vector<int> packet = {1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0}; 
    vector<int> crc = calculateCRC(packet, generator);
    cout << "CRC для исходного пакета: ";
    printVector(crc);

    // Добавляем остаток CRC в пакет (передача с CRC)
    vector<int> transmittedPacket = packet;
    transmittedPacket.insert(transmittedPacket.end(), crc.begin(), crc.end());

    cout << "Пакет с добавленным CRC: ";
    printVector(transmittedPacket);

    vector<int> remainder = calculateCRC(transmittedPacket, generator);
    
    cout << "Остаток на приемной стороне: ";
    printVector(remainder);
    
    if (all_of(remainder.begin(), remainder.end(), [](int bit) { return bit == 0; })) {
        cout << "Нет ошибок в принятом пакете." << endl;
    } else {
        cout << "Ошибка в принятом пакете!" << endl;
    }

    return 0;
}
