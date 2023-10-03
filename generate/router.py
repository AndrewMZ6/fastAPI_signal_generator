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
