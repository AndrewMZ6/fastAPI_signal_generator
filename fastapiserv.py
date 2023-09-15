from typing import Union
from fastapi import FastAPI
import numpy as np
import commpy as cp
import json
from pydantic import BaseModel

app = FastAPI()


def IDFT(s):
    return np.fft.ifft(s)

def DFT(t):
    return np.fft.fft(t)

def SHIFT(s):
    return np.fft.fftshift(s)


class my_item(BaseModel):
    name: str
    description: str | None = None
    price: float 
    tax: float | None = None
    tags: list[str] = []


def generate_ofdm_nopilots(fftsize_arg, NN):
    gsize = 100    
    fftsize = fftsize_arg

    K = fftsize - 2*gsize - 1 + 1  # -1 of central zero, and +1 of right guard

    # bits per symbol
    mu = NN

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


def generate_ofdm_withpilots(fftsize_arg, NN):
    gsize = 100   
    fftsize = fftsize_arg
    P = 200

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
    mu = NN

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



@app.get("/OFDM/{fftsize}/{Modulation_order}")
async def read_root(fftsize, Modulation_order):

    arr = generate_ofdm_nopilots(int(fftsize), int(Modulation_order))
    arr_r = json.dumps(arr.real.tolist())
    arr_im = json.dumps(arr.imag.tolist())
    return {'answer':{'real':arr_r, 'imag':arr_im}}



@app.get("/pOFDM/{fftsize}/{Modulation_order}")
async def read_root_p(fftsize, Modulation_order):

    arr, a, c = generate_ofdm_withpilots(int(fftsize), int(Modulation_order))
    arr_r = json.dumps(arr.real.tolist())
    arr_im = json.dumps(arr.imag.tolist())

    return {'answer':{'real':arr_r, 'imag':arr_im}}