function gold_sequence = generateGoldSequence(x, y, length)
    x_reg = zeros(1, 5);
    y_reg = zeros(1, 5);
    
    % Инициализация регистров сдвига
    x_reg(1:5) = bitget(x, 5:-1:1);
    y_reg(1:5) = bitget(y, 5:-1:1);

    gold_sequence = zeros(1, length);

    % Генерация последовательности
    for i = 1:length
        output = mod(x_reg(5) + y_reg(5), 2);
        gold_sequence(i) = output;

        new_x = mod(x_reg(1) + x_reg(4), 2); % X4, X5
        new_y = mod(y_reg(2) + y_reg(5), 2); % Y2, Y5

        x_reg = [new_x, x_reg(1:4)];
        y_reg = [new_y, y_reg(1:4)];
    end
end
