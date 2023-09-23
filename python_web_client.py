import requests
import numpy as np
import json
from matplotlib import pyplot as plt

method = 'GET'
fftsize = 1024
modulation_order = 16
bw = 5e6
fs = 50e6
url = f'http://127.0.0.1:8088/ofdm_fft_bw_fs/{fftsize}/{modulation_order}/{bw}/{fs}'



response = requests.request(method, url)
h = response.json()
c = json.loads(h)
arr = np.array(list(map(complex, c)), dtype=complex)



if __name__ == '__main__':

	plt.plot(abs(np.fft.fft(arr)))
	plt.show()