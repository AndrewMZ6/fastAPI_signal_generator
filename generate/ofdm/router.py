from fastapi import APIRouter, Path as fastApiPath, HTTPException
from typing_extenstions import Annotated
from pathlib import Path
import sys
path = Path(__file__).parents[1]
sys.path.append(str(path))
from services.operations_dispatcher import op_dispatcher as operations_dispatcher
from .pydantic_models import FftsizeMorder
import numpy as np


router = APIRouter()


@router.get('/')
async def index():
	array1 = [6.13, 5.8, 9.135, 1.513]
	array2 = [2.75, -4.64, -1.83, 8.1]
	L = np.vectorize(complex)(array1, array2)
	return {'response':{'real':L.real.tolist(), 'imag':L.imag.tolist()}}


@router.get('/complex/fftsize/{fftsize}/morder/{modulation_order}')
async def get_ofdm_no_pilots(
								fftsize: Annotated[int, fastApiPath(ge=0, le=50000)], 
								modulation_order: Annotated[int, fastApiPath(ge=4, le=256)]
							):

	request_parameters = FftsizeMorder(fftsize=fftsize, morder=modulation_order)
	response = operations_dispatcher.generate(request_parameters)
	return response


@router.get('/real/fftsize/{fftsize}/morder/{modulation_order}/bw/{BW}/fs/{fs}/fc/{fc}')
async def get_ofdm_fft_bw_fs(fftsize: int, modulation_order: int, BW: float, fs: float, fc: float):
	request_parameters = {
		'fftsize':fftsize,
		'modulation_order':modulation_order,
		'bw':BW,
		'fs':fs,
		'fc':fc
	}
	response = operations_dispatcher.generate(request_parameters)
	return response



if __name__ == '__main__':
	print(FftsizeMorder)
	help(HTTPException)