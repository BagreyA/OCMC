#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

// Функция для генерации последовательности Голда
vector<int> generateGoldSequence(int x, int y, int length) {
    vector<int> sequence;
    vector<int> x_reg(5), y_reg(5);

    // Инициализация регистров сдвига
    for (int i = 0; i < 5; ++i) {
        x_reg[i] = (x >> (4 - i)) & 1; // Инициализация регистра X
        y_reg[i] = (y >> (4 - i)) & 1; // Инициализация регистра Y
    }

    // Генерация последовательности
    for (int i = 0; i < length; ++i) {
        int output = x_reg[4] ^ y_reg[4]; // Выходной бит
        sequence.push_back(output);

        // Новые биты для регистров
        int new_x = (x_reg[0] ^ x_reg[3]); // X4, X5
        int new_y = (y_reg[1] ^ y_reg[4]); // Y2, Y5

        // Сдвиг регистров
        for (int j = 4; j > 0; --j) {
            x_reg[j] = x_reg[j - 1];
            y_reg[j] = y_reg[j - 1];
        }

        x_reg[0] = new_x; // Обновляем регистр X
        y_reg[0] = new_y; // Обновляем регистр Y
    }

    return sequence;
}

// Функция для вычисления автокорреляции
double calculateAutocorrelation(const vector<int>& seq1, const vector<int>& seq2) {
    int n = seq1.size();
    int correlation = 0;

    for (int i = 0; i < n; ++i) {
        int val1 = (seq1[i] == 0) ? -1 : 1;
        int val2 = (seq2[i] == 0) ? -1 : 1;
        correlation += val1 * val2;
    }

    return static_cast<double>(correlation) / n;
}

// Функция для циклического сдвига
vector<int> cyclicShift(const vector<int>& sequence, int shift) {
    int n = sequence.size();
    vector<int> shifted(n);
    for (int i = 0; i < n; ++i) {
        shifted[i] = sequence[(i + shift) % n];
    }
    return shifted;
}

// Функция для взаимной корреляции
double calculateCrossCorrelation(const vector<int>& seq1, const vector<int>& seq2) {
    int n = seq1.size();
    int correlation = 0;

    for (int i = 0; i < n; ++i) {
        int val1 = (seq1[i] == 0) ? -1 : 1;
        int val2 = (seq2[i] == 0) ? -1 : 1;
        correlation += val1 * val2;
    }

    return static_cast<double>(correlation) / n;
}

int main() {
    int x1 = 3;
    int y1 = x1 + 7;
    int x2 = x1 + 1;
    int y2 = y1 - 5;

    int length = 31;

    // Генерация первой последовательности
    vector<int> goldSequence1 = generateGoldSequence(x1, y1, length);
    cout << "Генерированная первая последовательность Голда:\n";
    for (int bit : goldSequence1) {
        cout << bit;
    }
    cout << endl;

    // Таблица автокорреляции для первой последовательности
    cout << setw(5) << "Сдвиг ";
    for (int i = 0; i < length; ++i) {
        cout << setw(2) << "Бит " << i + 1 << " ";
    }
    cout << setw(20) << "   С исходной " << setw(20) << "  С предыдущим шагом" << endl;

    vector<int> previousShiftedSequence = goldSequence1; // Инициализация для начального шага
    for (int shift = 0; shift < length; ++shift) {
        vector<int> shiftedSequence1 = cyclicShift(goldSequence1, shift);
        
        // Расчет автокорреляции
        double autocorrelationWithOriginal = calculateAutocorrelation(shiftedSequence1, goldSequence1);
        double autocorrelationWithPrevious = (shift == 0) ? 1.0 : calculateAutocorrelation(shiftedSequence1, previousShiftedSequence);

        // Вывод результатов
        cout << setw(5) << shift;
        for (int bit : shiftedSequence1) {
            cout << setw(3) << bit;
        }
        cout << setw(20) << fixed << setprecision(6) << autocorrelationWithOriginal;
        cout << setw(20) << fixed << setprecision(6) << autocorrelationWithPrevious << endl;

        previousShiftedSequence = shiftedSequence1; // Обновляем для следующего сдвига
    }

    // Генерация второй последовательности
    vector<int> goldSequence2 = generateGoldSequence(x2, y2, length);
    cout << "\nГенерированная вторая последовательность Голда:\n";
    for (int bit : goldSequence2) {
        cout << bit;
    }
    cout << endl;

    // Таблица автокорреляции для второй последовательности
    cout << "\nТаблица автокорреляции для второй последовательности:\n";
    cout << setw(5) << "Сдвиг ";
    for (int i = 0; i < length; ++i) {
        cout << setw(2) << "Бит " << i + 1 << " ";
    }
    cout << setw(20) << "   С исходной  " << setw(20) << "    С предыдущим шагом" << endl;

    previousShiftedSequence = goldSequence2; // Сброс для второй последовательности
    for (int shift = 0; shift < length; ++shift) {
        vector<int> shiftedSequence2 = cyclicShift(goldSequence2, shift);
        
        // Расчет автокорреляции
        double autocorrelationWithOriginal = calculateAutocorrelation(shiftedSequence2, goldSequence2);
        double autocorrelationWithPrevious = (shift == 0) ? 1.0 : calculateAutocorrelation(shiftedSequence2, previousShiftedSequence);

        // Вывод результатов
        cout << setw(5) << shift;
        for (int bit : shiftedSequence2) {
            cout << setw(3) << bit;
        }
        cout << setw(20) << fixed << setprecision(6) << autocorrelationWithOriginal;
        cout << setw(20) << fixed << setprecision(6) << autocorrelationWithPrevious << endl;

        previousShiftedSequence = shiftedSequence2; // Обновляем для следующего сдвига
    }

    // Вычисление взаимной корреляции
    double crossCorrelation = calculateCrossCorrelation(goldSequence1, goldSequence2);
    cout << "\nЗначение взаимной корреляции: " << fixed << setprecision(6) << crossCorrelation << endl;

    return 0;
}