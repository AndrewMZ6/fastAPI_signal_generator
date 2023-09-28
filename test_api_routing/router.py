from fastapi import APIRouter
from .test_further.router import router as frouter


router = APIRouter()
router.include_router(prefix='/further', router=frouter)


@router.get('/')
async def index():
	return {'response':f'{__file__=}'}