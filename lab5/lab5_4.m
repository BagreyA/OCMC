function lab5_4()
    rng('shuffle'); % Инициализация генератора случайных чисел
    generator2 = {[1,1,0,1],[1,1,0,1,0,0,1],[1,1,0,1,0,0,0,1,0,1]};
    
    % Создаем массив для хранения значений errorsNotDetected для каждого размера пакета
    errorsNotDetectedArray = cell(1, 3); % Для каждого генератора

    for generator_number = 1:3
        errorsNotDetectedArray{generator_number} = []; % Инициализация массива для текущего генератора
        
        for j = 10:100:2010
            packet = generate_packet(j);
            crc2 = calculateCRC(packet, generator2{generator_number});
            packetWithCRC = appendCRC(packet, crc2);

            if checkPacket(packetWithCRC, generator2{generator_number})
                fprintf('Ошибок не обнаружено в принятом пакете.\n');
            else
                fprintf('Ошибка обнаружена в принятом пакете.\n');
            end

            errorsDetected = 0;
            errorsNotDetected = 0;

            for i = 1:length(packet)
                % Искажение бита
                packetWithCRC(i) = mod(packetWithCRC(i) + 1, 2);

                % Проверка на приемной стороне
                if checkPacket(packetWithCRC, generator2{generator_number})
                    errorsNotDetected = errorsNotDetected + 1;
                else
                    errorsDetected = errorsDetected + 1;
                end

                % Восстановление бита
                %packetWithCRC(i) = mod(packetWithCRC(i) + 1, 2);
            end

            fprintf('Количество обнаруженных ошибок: %d\n', errorsDetected);
            fprintf('Количество необнаруженных ошибок: %d\n', errorsNotDetected);
            
            % Сохраняем количество необнаруженных ошибок в массив
            errorsNotDetectedArray{generator_number} = [errorsNotDetectedArray{generator_number}, errorsNotDetected];
        end
        
        % Построение графика для текущего генератора
        figure();
        plot(10:100:2010, errorsNotDetectedArray{generator_number}, '-o');
        title(['Errors Not Detected for Generator ' num2str(generator_number)]);
        xlabel('Packet Length');
        ylabel('Errors Not Detected');
        grid on;
    end
end

function N_sequence = generate_packet(packet_length)
    N_sequence = randi([0, 1], 1, packet_length);
end

function crc = calculateCRC(packet, generator)
    temp = [packet, zeros(1, length(generator) - 1)];
    generatorSize = length(generator);

    for i = 1:length(temp) - generatorSize + 1
        if temp(i) == 1
            temp(i:i + generatorSize - 1) = mod(temp(i:i + generatorSize - 1) + generator, 2);
        end
    end

    crc = temp(end - (generatorSize - 2):end);
end

function result = appendCRC(packet, crc)
    result = [packet, crc];
end

function isValid = checkPacket(packetWithCRC, generator)
    remainder = calculateCRC(packetWithCRC, generator);
    isValid = all(remainder == 0);
end
