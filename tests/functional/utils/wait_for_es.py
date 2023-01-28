import time

from elasticsearch import Elasticsearch

from settings import app_settings

if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{app_settings.elastic_host}:{app_settings.elastic_port}',
        validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
