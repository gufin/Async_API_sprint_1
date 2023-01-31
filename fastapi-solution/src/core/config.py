import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = 'movies'

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    elastic_host: str = '127.0.0.1'
    elastic_port: int = 9200
    redis_url: str = 'redis://127.0.0.1:6379'

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    cache_expire_in_seconds: int = 300

    class Config:
        env_file = '.env'


app_settings = AppSettings()
