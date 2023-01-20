import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import BaseSettings, Field
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    PROJECT_NAME = Field('movies', env='PROJECT_NAME')

    REDIS_HOST = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT = Field(6379, env='REDIS_PORT')

    ELASTIC_HOST = Field('127.0.0.1', env='ELASTIC_HOST')
    ELASTIC_PORT = Field(9200, env='ELASTIC_PORT')

    base_dir: str = Field(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env='BASE_DIR')
    CACHE_EXPIRE_IN_SECONDS = 300

    class Config:
        env_file = '.env'


app_settings = AppSettings()
