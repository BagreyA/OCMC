#include <iostream>
#include <vector>

using namespace std;

// Порождающий полином G = x^7+x^6+x^5+x^3+x^2+x+1
vector<int> generator = {1, 1, 1, 0, 1, 1, 1};

// Функция для вычисления CRC
vector<int> calculateCRC(const vector<int>& packet, const vector<int>& generator) {
    vector<int> temp(packet);
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
void printVector(const vector<int>& vec) {
    for (int bit : vec) {
        cout << bit;
    }
    cout << endl;
}

int main() {
//    vector<int> packet = {1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0}; 
    vector<int> packet(250);
    for (int i = 0; i < 250; ++i) {
        packet[i] = rand() % 2;
    }

    vector<int> crc = calculateCRC(packet, generator);
    
    cout << "CRC для исходного пакета: ";
    printVector(crc);

    return 0;
}
