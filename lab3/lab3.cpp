#include <iostream>
#include <cmath>
using namespace std;

// Размер массивов
#define N 8

// Функция для вычисления корреляции
double correlation(int x[], int y[], int n) {
    double corr = 0;
    for (int i = 0; i < n; i++) {
        corr += x[i] * y[i];
    }
    return corr;
}

// Функция для вычисления нормализованной корреляции
double normalizedCorrelation(int x[], int y[], int n) {
    double numerator = 0, sumX2 = 0, sumY2 = 0;
    for (int i = 0; i < n; i++) {
        numerator += x[i] * y[i];
        sumX2 += x[i] * x[i];
        sumY2 += y[i] * y[i];
    }
    return numerator / (sqrt(sumX2) * sqrt(sumY2));
}

// Главная функция
int main() {
    int a[N] = {6, 2, 8, -2, -4, -4, 1, 3};
    int b[N] = {3, 6, 7, 0, -5, -4, 2, 5};
    int c[N] = {-1, -1, 3, -9, 2, -8, 4, -1};

    // Вычисление корреляции
    double corr_ab = correlation(a, b, N);
    double corr_ac = correlation(a, c, N);
    double corr_bc = correlation(b, c, N);

    // Вычисление нормализованной корреляции
    double normCorr_ab = normalizedCorrelation(a, b, N);
    double normCorr_ac = normalizedCorrelation(a, c, N);
    double normCorr_bc = normalizedCorrelation(b, c, N);

    // Вывод результатов
    cout << "Корреляция между a, b и c:" << endl;
    cout << "\t| a\t| b\t| c" << endl;
    cout << "a\t| -\t| " << corr_ab << "\t| " << corr_ac << endl;
    cout << "b\t| " << corr_ab << "\t| -\t| " << corr_bc << endl;
    cout << "c\t| " << corr_ac << "\t| " << corr_bc << "\t| -" << endl;

    cout << "Нормализованная корреляция между a, b и c:" << endl;
    cout << "\t| a\t| b\t| c" << endl;
    cout << "a\t| -\t| " << normCorr_ab << "\t| " << normCorr_ac << endl;
    cout << "b\t| " << normCorr_ab << "\t| -\t| " << normCorr_bc << endl;
    cout << "c\t| " << normCorr_ac << "\t| " << normCorr_bc << "\t| -" << endl;

    return 0;
}
