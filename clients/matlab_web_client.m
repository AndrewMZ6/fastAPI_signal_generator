%% Load complex array to api and get FFT of it
clc; close all; clearvars;

bits = randi([0, 1], 10000, 1);
signal_to_load = qammod(bits, 16, 'InputType', 'bit');
real_data = real(signal_to_load).';
imag_data = imag(signal_to_load).';


request_body = jsonencode(struct('complex', true, 'real_data', real_data, 'imag_data', imag_data));
options = weboptions('MediaType', 'application/json');


x = webwrite('https://ofdm-buddy.onrender.com/get_fft', request_body, options);

y = cellfun(@str2double, jsondecode(x));

y_matlab = fft(signal_to_load);

figure;
    plot(abs(xcorr(y, y2_matlab)));
    title('correlation of matlab fft and fastapi fft');
    
    
%% Acquire ofdm symbol without pilots
close all; clearvars; clc;

modulation_order = 16;
fftsize = 1024;
endpoint_url = 'https://ofdm-buddy.onrender.com/OFDM/';


api_url = [endpoint_url, num2str(fftsize), '/', num2str(modulation_order)];
response = cellfun(@str2double, jsondecode(webread(api_url)));


figure;
    plot(abs(fft(response)));
    
scatterplot(fft(response));


%% Acquire ofdm symbol without pilots
close all; clearvars; clc;

modulation_order = 4;
fftsize = 1024;
bw = 2e6;
fs = 10e6;


endpoint_url = 'https://ofdm-buddy.onrender.com/ofdm_fft_bw_fs/';


api_url = [endpoint_url, num2str(fftsize), '/', num2str(modulation_order), '/', num2str(bw), '/', num2str(fs)];
response = cellfun(@str2double, jsondecode(webread(api_url)));
response_len = length(response);
freqline = (fs/response_len:fs/response_len:fs)*1e-6;

figure;
    plot(freqline, abs(fft(response)));
    xlabel('freq, MHz');
    
scatterplot(fft(response));




