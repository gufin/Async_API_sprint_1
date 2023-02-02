import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = "movies"

    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_url: str = f"redis://{redis_host}:{redis_port}"

    elastic_host: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
    elastic_port: int = os.getenv("ELASTIC_PORT", 9200)

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    cache_expire_in_seconds: int = 300

    class Config:
        env_file = ".env"


app_settings = AppSettings()
