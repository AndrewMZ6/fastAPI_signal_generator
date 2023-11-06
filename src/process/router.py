from fastapi import APIRouter

router = APIRouter()

@router.get('/fft')
async def correlate_signals():
	response = operations_dispatcher.process(data, 'fft')
	return response
