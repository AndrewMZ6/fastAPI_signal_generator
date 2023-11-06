from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class Somemodel(BaseModel):
	name: str
	age: int | None
	description: str | None




@router.get('/')
async def index(x: int = 10, operation: str = 'summ'):
	return {'response':f'further testing index'}


@router.post('/')
async def index_post(data: Somemodel):
	return {'response': f'{Somemodel = }'}