from fastapi import APIRouter
from data_processing.process_data import get_ofdm_fftsize_modorder, get_ofdm_fft_bw_fs


router = APIRouter()


@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'process page'
	}


@router.get('/correlate')
async def correlate_signals(data: DataModel):
	response = operations_dispatcher.process(data, 'correlate')
    return response
