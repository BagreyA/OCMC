% Основной код
x1 = 3;
y1 = x1 + 7;
x2 = x1 + 1;
y2 = y1 - 5;
length = 31;

% Генерация последовательностей
goldSequence1 = generateGoldSequence(x1, y1, length);
goldSequence2 = generateGoldSequence(x2, y2, length);

disp('Первая последовательность Голда:');
disp(goldSequence1);

disp('Вторая последовательность Голда:');
disp(goldSequence2);


% Вычисление автокорреляции
autocorr1 = autocorr(goldSequence1, 'NumLags', length - 1);
autocorr2 = autocorr(goldSequence2, 'NumLags', length - 1);

% Вычисление взаимной корреляции
cross_corr = xcorr(goldSequence1, goldSequence2, 'coeff');

% Создание векторов задержки (lag)
lags = 0:length - 1;

% Вывод результатов
disp('Автокорреляция первой последовательности:');
disp(autocorr1');

disp('Автокорреляция второй последовательности:');
disp(autocorr2');

disp('Взаимная корреляция между последовательностями:');
disp(cross_corr);


% Визуализация автокорреляции
figure;
subplot(2, 1, 1);
stem(lags, autocorr1, 'filled');
title('Автокорреляция первой последовательности');
xlabel('Задержка (lag)');
ylabel('Автокорреляция');
grid on;

subplot(2, 1, 2);
stem(lags, autocorr2, 'filled');
title('Автокорреляция второй последовательности');
xlabel('Задержка (lag)');
ylabel('Автокорреляция');
grid on;
