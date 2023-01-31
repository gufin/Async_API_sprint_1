import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    project_name: str = "movies"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    elastic_host: str = "127.0.0.1"
    elastic_port: int = 9200
    elastic_url: str = "http://127.0.0.1:9200"
    service_url: str = "http://127.0.0.1:8001"
    service_api_url: str = f"{service_url}/api/v1"
    redis_url: str = "redis://127.0.0.1:6379"

    base_api: str = "http://127.0.0.1:8000/api/v1"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    cache_expire_in_seconds: int = 300

    class Config:
        env_file = ".env"


app_settings = AppSettings()
