from fastapi import APIRouter
from .ofdm.router import router as ofdm_router


router = APIRouter()
router.include_router(prefix='/ofdm', router=ofdm_router)

@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'index'
	}

'''
@router.get('/ofdm{fftsize}/{Modulation_order}')
async def get_ofdm_no_pilots(fftsize: int, Modulation_order: int):
    response = get_ofdm_fftsize_modorder(fftsize, Modulation_order)

    return response


@router.get('/complex/{fftsize}/{Modulation_order}/{BW}/{fs}/{fc}')
async def get_ofdm_fft_bw_fs(fftsize: int, Modulation_order: int, BW: float, fs: float, fc: float):
	response = await get_ofdm_fft_bw_fs(fftsize, Modulation_order, BW, fs, fc)

	return response

'''