import uvicorn
from typing import Union, Any
from fastapi import FastAPI, Request, Body
import numpy as np
import json
from settings.settings import settings
from pydantic import BaseModel
from generate.router import router as generate_router
from process.router import router as process_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='Ofdm buddy')


origins = ['*']

app.add_middleware(middleware_class=CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   )


app.include_router(prefix='/generate', router=generate_router)
app.include_router(prefix='/process', router=process_router)


@app.get('/')
async def index():
    return {'page':'index'}

