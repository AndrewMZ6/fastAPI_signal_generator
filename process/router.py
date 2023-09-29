from fastapi import APIRouter



router = APIRouter()


@router.get('/')
async def index():
	return {
		'status':'success',
		'page':'process page'
	}


@router.get('/correlate')
async def correlate_signals():
	response = operations_dispatcher.process(data, 'correlate')
	return response
