clc; close all; clearvars;

bits = randi([0, 1], 100, 1);
signal_to_load = qammod(bits, 16, 'InputType', 'bit');
real_data = real(signal_to_load).';
imag_data = imag(signal_to_load).';


request_body = jsonencode(struct('complex', true, 'real_data', real_data, 'imag_data', imag_data));
options = weboptions('MediaType', 'application/json');


x = webwrite('http://127.0.0.1:8088/get_fft', request_body, options);

y = cellfun(@str2double, jsondecode(x));

y_matlab = fft(signal_to_load);

figure;
    plot(abs(xcorr(y, y_matlab)));
    title('ello');