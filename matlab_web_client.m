%% Load complex array to api and get FFT of it
clc; close all; clearvars;

bits = randi([0, 1], 10000, 1);
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
    title('correlation of matlab fft and fastapi fft');
    
    
%% Acquire ofdm symbol without pilots
close all; clearvars; clc;

modulation_order = 16;
fftsize = 1024;
endpoint_url = 'http://127.0.0.1:8088/OFDM/';


api_url = [endpoint_url, num2str(fftsize), '/', num2str(modulation_order)];
response = cellfun(@str2double, jsondecode(webread(api_url)));


figure;
    plot(abs(fft(response)));
    
scatterplot(fft(response));


%% Acquire ofdm symbol without pilots
close all; clearvars; clc;

modulation_order = 64;
fftsize = 1024;
bw = 5e6;
fs = 50e6;


endpoint_url = 'http://127.0.0.1:8088/ofdm_fft_bw_fs/';


api_url = [endpoint_url, num2str(fftsize), '/', num2str(modulation_order), '/', num2str(bw), '/', num2str(fs)];
response = cellfun(@str2double, jsondecode(webread(api_url)));
response_len = length(response);
freqline = (fs/response_len:fs/response_len:fs)*1e-6;

figure;
    plot(freqline, abs(fft(response)));
    xlabel('freq, MHz');
    
scatterplot(fft(response));