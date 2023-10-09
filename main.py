from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from generate.router import router as generate_router
from process.router import router as process_router
from frontend.router import router as frontend_router


app = FastAPI(title='Ofdm buddy')


origins = ['*']
app.add_middleware(middleware_class=CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   )


app.mount(path=f'/static', app=StaticFiles(directory=f'static'), name='static')

app.include_router(prefix='/generate', router=generate_router)
app.include_router(prefix='/process', router=process_router)
app.include_router(prefix='/frontend/v1', router=frontend_router)


@app.get('/')
async def index():
    return {'page':'index'}
