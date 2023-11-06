from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pathlib


router = APIRouter()
STATIC_PATH = str(pathlib.Path(__file__).parent.parent.resolve())


templates = Jinja2Templates(directory='frontend')


@router.get('/')
def index(request: Request):
	return templates.TemplateResponse('some_cool_frontend.html', {"request": request})