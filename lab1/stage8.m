[y, Fs] = audioread('baia-232.wav');

Y = fft(y); 
N = length(Y);
f = (0:N-1)*(Fs/N);
amplitude_spectrum_Y = abs(Y);

downsample_factor = 10;  
y1 = downsample(y, downsample_factor);  
new_Fs = Fs / downsample_factor;  

Y1 = fft(y1); 
N1 = length(Y1); 
f1 = (0:N1-1)*(new_Fs/N1); 
amplitude_spectrum_Y1 = abs(Y1); 

figure;

% Оригинальный сигнал
subplot(2, 1, 1);
plot(f, amplitude_spectrum_Y);
title('Амплитудный спектр оригинального сигнала');
xlabel('Частота (Гц)');
ylabel('Амплитуда');
xlim([0 Fs/2]); % Ограничиваем ось X до половины частоты дискретизации
grid on;

% Прореженный сигнал
subplot(2, 1, 2);
plot(f1, amplitude_spectrum_Y1);
title('Амплитудный спектр прореженного сигнала');
xlabel('Частота (Гц)');
ylabel('Амплитуда');
xlim([0 new_Fs/2]); 
grid on;

threshold = 0.01 * max(amplitude_spectrum_Y); % Устанавливаем порог
width = f(find(amplitude_spectrum_Y > threshold, 1, 'last')) - ...
        f(find(amplitude_spectrum_Y > threshold, 1, 'first')); % Ширина для оригинального сигнала

% Ширина для прореженного сигнала
width1 = f1(find(amplitude_spectrum_Y1 > threshold, 1, 'last')) - ...
         f1(find(amplitude_spectrum_Y1 > threshold, 1, 'first')); % Ширина для прореженного сигнала

disp(['Ширина амплитудного спектра оригинального сигнала: ', num2str(width), ' Гц']);
disp(['Ширина амплитудного спектра прореженного сигнала: ', num2str(width1), ' Гц']);
