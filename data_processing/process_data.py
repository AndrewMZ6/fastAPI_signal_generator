import numpy as np
import json
import commpy as cp


def IDFT(s):
    return np.fft.ifft(s)


def DFT(t):
    return np.fft.fft(t)


def SHIFT(s):
    return np.fft.fftshift(s)


def np_complex_arr_to_json(complex_data: np.ndarray) -> str:
    L = complex_data.tolist()

    # original list looks like this [(-3+3j), (-3+3j), (1-3j)] so [1:-1] removes bracets
    M = list(map(lambda x: str(x)[1:-1], L))
    response = json.dumps(M)

    return response


def generate_ofdm_nopilots(fftsize: int, M_order: int) -> np.ndarray:
    gsize = 100

    K = fftsize - 2*gsize - 1 + 1  # -1 of central zero, and +1 of right guard

    # bits per symbol
    mu = int(np.log2(M_order))

    # number of payload bits per OFDM symbol
    payLoadBits_per_OFDM = K*mu

    # generate random bits
    bits = np.random.randint(low=0, high=2, size=payLoadBits_per_OFDM)

    # modulate
    M = cp.modulation.QAMModem(2**mu)
    modBits = M.modulate(bits)

    ofdmSymbol = np.concatenate([np.zeros(gsize, dtype=complex), modBits[:int(K/2)], np.zeros(1, dtype=complex), modBits[int(K/2):], np.zeros(gsize-1, dtype=complex)])

    ofdmSymbolShifted = SHIFT(ofdmSymbol)
    ofdm_time = IDFT(ofdmSymbolShifted)

    # return time samples
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


