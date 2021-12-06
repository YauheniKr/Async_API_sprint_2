from pydantic import BaseSettings
from pydantic.parse import Path

BASE_DIR = Path(__file__).resolve().parent
TESTDATA_DIR = Path(*[BASE_DIR / 'testdata' / 'data'])
SCHEMA_DIR = Path(*[BASE_DIR / 'testdata' / 'schema'])
UTILS_DIR = [BASE_DIR / 'utils']


class TestSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = 'elasticsearch'
    ELASTIC_PORT: int = 9200

    # Настройки сервиса
    SERVICE_HOST: str = 'async_api'
    SERVICE_PORT: int = 8000

    class Config:
        case_sensitive = True


test_settings = TestSettings()
