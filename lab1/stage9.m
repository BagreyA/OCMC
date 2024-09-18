function quantization_effect()
    
    Fs = 8000;
    t = 0:1/Fs:1;
    f_signal = 6; 
    original_signal = 4 * sin(2 * pi * f_signal * t + pi/3);

    bit_depths = [3, 4, 5, 6];

    for bits = bit_depths
        quantized_signal = quantize_signal(original_signal, bits);
        
        Y = fft(original_signal);
        Y_quantized = fft(quantized_signal);
        
        amplitude_spectrum = abs(Y);
        amplitude_spectrum_quantized = abs(Y_quantized);
        
        amplitude_spectrum = amplitude_spectrum / max(amplitude_spectrum);
        amplitude_spectrum_quantized = amplitude_spectrum_quantized / max(amplitude_spectrum_quantized);
       
        quantization_error = original_signal - quantized_signal;
        mean_quantization_error = mean(abs(quantization_error));
        
        f = (0:length(original_signal)-1) * (Fs / length(original_signal));
        
        figure;
        plot(f(1:length(amplitude_spectrum)/2), amplitude_spectrum(1:length(amplitude_spectrum)/2), 'b', 'DisplayName', 'Оригинальный сигнал');
        hold on;
        plot(f(1:length(amplitude_spectrum_quantized)/2), amplitude_spectrum_quantized(1:length(amplitude_spectrum_quantized)/2), 'r', 'DisplayName', sprintf('Квантованный сигнал (биты = %d)', bits));
        hold off;
        title(sprintf('Сравнение амплитудных спектров для %d бит', bits));
        xlabel('Частота (Гц)');
        ylabel('Нормализованная амплитуда');
        xlim([0 Fs/2]);
        legend show;
        grid on;

        fprintf('Средняя ошибка квантования для %d бит: %.4f\n', bits, mean_quantization_error);
    end
end

function quantized_signal = quantize_signal(signal, bits)
    
    max_value = 4; 
    min_value = -4; 

    levels = 2^bits;

    scaled_signal = (signal - min_value) / (max_value - min_value) * (levels - 1);
    scaled_signal = round(scaled_signal);
    scaled_signal(scaled_signal >= levels) = levels - 1; 
    quantized_signal = scaled_signal / (levels - 1) * (max_value - min_value) + min_value; 
end

