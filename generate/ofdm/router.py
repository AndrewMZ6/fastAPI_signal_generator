from fastapi import APIRouter
from pathlib import Path
import sys
path = Path().cwd().parent.parent
print(path)
print(sys.path)
sys.path.append(str(path))
from services.operations_dispatcher import op_dispatcher as operations_dispatcher


router = APIRouter()


@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'index'
	}

@router.get('/complex/fftsize/{fftsize}/morder/{modulation_order}')
async def get_ofdm_no_pilots(fftsize: int, modulation_order: int):
	request_parameters = {
		'fftsize':fftsize,
		'modulation_order':modulation_order
	}
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
	import sys
	print(sys.path)