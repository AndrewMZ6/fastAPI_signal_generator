from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_host = '127.0.0.1'
    app_port = 8088


settings = Settings()