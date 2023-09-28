from fastapi import APIRouter
from services.operations_dispatcher import operations_dispatcher


router = APIRouter()


@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'index'
	}

@router.get('complex/fftsize/{fftsize}/morder/{modulation_order}')
async def get_ofdm_no_pilots(fftsize: int, modulation_order: int):
	request_parameters = {
		'fftsize':fftsize,
		'modulation_order':modulation_order
	}
	response = await operations_dispatcher.generate(request_parameters)
	return response

@router.get('real/fftsize/{fftsize}/morder/{modulation_order}/bw/{BW}/fs/{fs}/fc/{fc}')
async def get_ofdm_fft_bw_fs(fftsize: int, modulation_order: int, BW: float, fs: float, fc: float):
	request_parameters = {
		'fftsize':fftsize,
		'modulation_order':modulation_order,
		'bw':BW,
		'fs':fs,
		'fc':fc
	}
	response = await operations_dispatcher.generate(request_parameters)
	return response



if __name__ == '__main__':
	import sys
	print(sys.path)