from fastapi import APIRouter
from data_processing.process_data import get_ofdm_fftsize_modorder, get_ofdm_fft_bw_fs


router = APIRouter()


@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'index'
	}


@router.get('/{fftsize}/{Modulation_order}')
async def get_ofdm_no_pilots(fftsize: int, Modulation_order: int):
    response = get_ofdm_fftsize_modorder(fftsize, Modulation_order)

    return response


@router.get('/complex/{fftsize}/{Modulation_order}/{BW}/{fs}/{fc}')
async def get_ofdm_fft_bw_fs(fftsize: int, Modulation_order: int, BW: float, fs: float, fc: float):
	response = await get_ofdm_fft_bw_fs(fftsize, Modulation_order, BW, fs, fc)

	return response