с[y, Fs] = audioread('baia-232.wav'); 

downsample_factor = 10; 
y1 = downsample(y, downsample_factor); 

zvuk = audioplayer(y1, Fs / downsample_factor);  

play(zvuk);

figure;  % Создаем новую фигуру
plot(y1);
xlabel('Отсчеты');  % Подпись оси X
ylabel('Амплитуда'); % Подпись оси Y
title('Прореженный сигнал'); 

output_filename = 'downsampled_signal.wav'; 
audiowrite(output_filename, y1, Fs / downsample_factor);  