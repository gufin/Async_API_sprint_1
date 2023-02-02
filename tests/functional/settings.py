import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    project_name: str = "movies"

    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_url: str = f"redis://{redis_host}:{redis_port}"

    elastic_host: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
    elastic_port: int = os.getenv("ELASTIC_PORT", 9200)
    elastic_url: str = f"http://{elastic_host}:{elastic_port}"

    fast_api_host: str = os.getenv("FAST_API_HOST", "127.0.0.1")
    fast_api_port: int = os.getenv("FAST_API_PORT", 8001)
    service_url: str = f"http://{fast_api_host}:{fast_api_port}"
    service_api_url: str = f"{service_url}/api/v1"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    cache_expire_in_seconds: int = 300

    CONNECTIONS_MAX_TIME = 60

    class Config:
        env_file = ".env"


app_settings = AppSettings()
