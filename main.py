import uvicorn
from typing import Union, Any
from fastapi import FastAPI, Request, Body
import numpy as np
import json
from settings.settings import settings
from pydantic import BaseModel
from generate.router import router as generate_router
from process.router import router as process_router


from data_processing.process_data import (
                                            generate_ofdm_nopilots,
                                            np_complex_arr_to_json,
                                            generate_ofdm_withpilots,
                                            addzeros,
                                            use_ofdm_carrier_signal,
                                            np_arr_to_json
                                          )



app = FastAPI(title='Ofdm buddy')
app.include_router(prefix='/generate', router=generate_router)
app.include_router(prefix='/process', router=process_router)



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
    complex_data = np.vectorize(complex)(data.real_data, data.imag_data)
    ffted_data = np.fft.fft(complex_data)
    response_data = np_complex_arr_to_json(ffted_data)

    return response_data


@app.get('/ofdm_fft_bw_fs/{fftsize}/{Modulation_order}/{BW}/{fs}')
async def get_ofdm_fft_bw_fs(fftsize: int, Modulation_order: int, BW: float, fs: float):
    arr = generate_ofdm_nopilots(fftsize, Modulation_order)
    interpolated_size = int((fs*fftsize)/BW)
    arr_interpolated = addzeros(arr, interpolated_size)
    response = np_complex_arr_to_json(np.fft.ifft(arr_interpolated))

    return response


@app.get('/ofdm_fft_bw_fs_carr/{fftsize}/{Modulation_order}/{BW}/{fs}/{fc}')
async def get_ofdm_fft_bw_fs(fftsize: int, Modulation_order: int, BW: float, fs: float, fc: float):
    arr = generate_ofdm_nopilots(fftsize, Modulation_order)
    interpolated_size = int((fs*fftsize)/BW)
    arr_interpolated = addzeros(arr, interpolated_size)
    carried_signal = use_ofdm_carrier_signal(arr_interpolated, fc, fs)
    response = np_arr_to_json(carried_signal)

    return response


@app.get('/get_error')
async def generate_error():
    error_message = {
            'error_status':'internal_error',
            'error_message':'too little to know'
    }

    return json.dumps(error_message)

# TODO:
#   1. look up some routing thingy
#   2. seek through pydantic models
#   3. may be improve matlab client interaction
#   4. add some database interaction 


# @app.get('/test-api/arg1')
# async def test_arg1():
#     return {'response':'test-arg1'}




# @app.get('/test-api')
# async def test1():
#     return {'response':'test1'}






if __name__ == '__main__':
    uvicorn.run(app=app, host=settings.app_host, port=settings.app_port, loop='auto')