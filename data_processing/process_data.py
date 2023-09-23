import numpy as np
import json
import commpy as cp


def IDFT(s):
    return np.fft.ifft(s)


def DFT(t):
    return np.fft.fft(t)


def SHIFT(s):
    return np.fft.fftshift(s)


def addzeros(sig: np.ndarray, interpolated_size: int) -> np.ndarray:
    spectrum = np.fft.fft(sig)
    L = len(spectrum)
    delimiter = int(L/2)
    zeros_to_insert = np.zeros(interpolated_size - L, dtype=complex)
    result = np.concatenate((spectrum[:delimiter], zeros_to_insert, spectrum[delimiter:]))
    return result


def use_ofdm_carrier_signal(signal_spectrum: np.ndarray, fc: float, fs: float) -> np.ndarray:
    time_domain_signal = np.fft.ifft(signal_spectrum)
    Ts = 1/fs
    timeline = np.arange(0, time_domain_signal.size*Ts, Ts)
    I_carr = np.cos(2*np.pi*fc*timeline)
    Q_carr = -np.sin(2*np.pi*fc*timeline)

    output = np.multiply(time_domain_signal.real, I_carr) + np.multiply(time_domain_signal.imag, Q_carr)

    return output


def np_arr_to_json(non_complex_data: np.ndarray) -> str:
    L = non_complex_data.tolist()
    M = list(map(lambda x: str(x), L))
    response = json.dumps(M)

    return response


def np_complex_arr_to_json(complex_data: np.ndarray) -> str:
    L = complex_data.tolist()
    M = list(map(lambda x: str(x)[1:-1], L))    # original list looks like this [(-3+3j), 
    response = json.dumps(M)                    # (-3+3j), (1-3j)] so [1:-1] removes bracets
    
    return response


def generate_ofdm_nopilots(fftsize: int, M_order: int) -> np.ndarray:
    gsize = 100

    K = fftsize - 2*gsize - 1 + 1                                           # -1 of central zero, and +1 of right guard
    mu = int(np.log2(M_order))                                              # bits per symbol
    payLoadBits_per_OFDM = K*mu                                             # number of payload bits per OFDM symbol
    bits = np.random.randint(low=0, high=2, size=payLoadBits_per_OFDM)      # generate random bits
    
    M = cp.modulation.QAMModem(2**mu)
    modBits = M.modulate(bits)
    ofdmSymbol = np.concatenate([np.zeros(gsize, dtype=complex), modBits[:int(K/2)], np.zeros(1, dtype=complex), modBits[int(K/2):], np.zeros(gsize-1, dtype=complex)])
    ofdmSymbolShifted = SHIFT(ofdmSymbol)
    ofdm_time = IDFT(ofdmSymbolShifted)

    return ofdm_time


def generate_ofdm_withpilots(fftsize: int, M_order: int, pilots_num: int) -> tuple:
    gsize = 100   
    P = pilots_num

    K = fftsize - 2*gsize - 1 + 1  # -1 of central zero, and +1 of right guard

    # indicies of all subcarriers
    allCarriers = np.arange(K)


    pilotStep = K//P

    # indicies of pilots
    pilotCarriers = allCarriers[::pilotStep]
    pilotValue = 2 + 2j

    pilotCarriers = np.hstack([pilotCarriers, np.array([allCarriers[-1]])])

    P = P + 1

    dataCarriers = np.delete(allCarriers, pilotCarriers)
    
    # bits per symbol
    mu = int(np.log2(M_order))

    # number of payload bits per OFDM symbol
    payLoadBits_per_OFDM = len(dataCarriers)*mu

    # generate random bits
    bits = np.random.randint(low=0, high=2, size=payLoadBits_per_OFDM)

    # modulate
    M = cp.modulation.QAMModem(2**mu)
    modBits = M.modulate(bits)

    # Put complex data to spectrum
    symbol = np.zeros(K, dtype=complex)
    symbol[pilotCarriers] = pilotValue
    symbol[dataCarriers] = modBits

    ofdmSymbol = np.concatenate([np.zeros(gsize, dtype=complex), symbol[:int(K/2)], np.zeros(1, dtype=complex), symbol[int(K/2):], np.zeros(gsize-1, dtype=complex)])

    ofdmSymbolShifted = SHIFT(ofdmSymbol)

    ofdm_time = IDFT(ofdmSymbolShifted)


    return ofdm_time, (pilotCarriers, dataCarriers), bits



def get_ofdm_fftsize_modorder(fftsize: int, Modulation_order: int):
    arr = generate_ofdm_nopilots(fftsize, Modulation_order)
    response = np_complex_arr_to_json(arr)

    return response


def get_ofdm_fft_bw_fs(fftsize: int, Modulation_order: int, BW: float, fs: float, fc: float):
    arr = generate_ofdm_nopilots(fftsize, Modulation_order)
    interpolated_size = int((fs*fftsize)/BW)
    arr_interpolated = addzeros(arr, interpolated_size)
    carried_signal = use_ofdm_carrier_signal(arr_interpolated, fc, fs)
    response = np_arr_to_json(carried_signal)

    return response