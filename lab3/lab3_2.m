% Параметры времени и частоты
f1 = 3; 
f2 = f1 + 4;
f3 = f1 * 2 + 1;
t = 0:0.01:1; % временной интервал

% Определение сигналов
s1 = cos(2 * pi * f1 * t);
s2 = cos(2 * pi * f2 * t);
s3 = cos(2 * pi * f3 * t);

% Сигналы a(t) и b(t)
a = 2 * s1 + 3 * s2 + s3;
b = s2 + s3;

% Вычисление корреляции
corr_ab = sum(a .* b);
norm_corr_ab = sum(a .* b) / (sqrt(sum(a.^2)) * sqrt(sum(b.^2)));

disp('Корреляция между сигналами a и b:');
disp(corr_ab);
disp('Нормализованная корреляция между сигналами a и b:');
disp(norm_corr_ab);
