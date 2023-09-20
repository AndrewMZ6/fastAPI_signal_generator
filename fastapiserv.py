from typing import Union, Any
from fastapi import FastAPI, Request, Body
import numpy as np
import json
from pydantic import BaseModel

from data_processing.process_data import (
                                            generate_ofdm_nopilots,
                                            np_complex_arr_to_json,
                                            generate_ofdm_withpilots

                                          )



app = FastAPI()



class Marray(BaseModel):
    boasdad: str
    arr: list



class Matlab_data(BaseModel):
    complex: bool
    real_data: list = []
    imag_data: list = []



@app.get("/OFDM/{fftsize}/{Modulation_order}")
async def get_ofdm_no_pilots(fftsize: int, Modulation_order: int):

    arr = generate_ofdm_nopilots(fftsize, Modulation_order)
    response = np_complex_arr_to_json(arr)

    return response



@app.get("/pOFDM/{fftsize}/{Modulation_order}/{pilots_num}")
async def read_root_t(fftsize: int, Modulation_order: int, pilots_num: int):

    arr, a, c = generate_ofdm_withpilots(fftsize, Modulation_order, pilots_num)
    response = np_complex_arr_to_json(arr)

    return response



@app.post('/process_integers/')
async def process_ofdm_data(data: Marray):
    
    print(data)
    print(data.boasdad)
    print(data.arr)
    print(type(data.arr))



@app.post('/post_marr/')
async def process_marr(data: Marray):
    payload = await data.body()
    decoded_payload = payload.decode('utf-8')
    print(decoded_payload)
    return payload



@app.post('/get_fft/')
async def get_fft(data: Matlab_data):

    # create one complex values array from two real values arrays
    complex_data = np.vectorize(complex)(data.real_data, data.imag_data)

    # make a simple fft operation
    ffted_data = np.fft.fft(complex_data)

    # convert complex numpy array into json format
    response_data = np_complex_arr_to_json(ffted_data)


    return response_data



# TODO:
#   1. look up some routing thingy
#   2. seek through pydantic models
#   3. may be improve matlab client interaction
#   4. add some database interaction 