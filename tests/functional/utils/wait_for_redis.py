import time

from redis import Redis

from settings import app_settings

if __name__ == "__main__":
    redis_client = Redis(
        host=app_settings.redis_host,
        port=app_settings.redis_port,
        socket_connect_timeout=1,
    )
    while not redis_client.ping():
        time.sleep(1)
