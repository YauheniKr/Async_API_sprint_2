import asyncio
import logging

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.etl_loader import ETLLoader
from tests.functional.settings import test_settings, SCHEMA_DIR, TESTDATA_DIR
from tests.functional.utils.models import HTTPResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def film_data_prepare():
    film_data = {
        'index': 'movies',
        'index_file': SCHEMA_DIR.joinpath('elastic_movies_schema.json'),
        'test_data': TESTDATA_DIR.joinpath('movies_test_data.json'),
    }
    return film_data


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((test_settings.REDIS_HOST,
                                              test_settings.REDIS_PORT), minsize=10, maxsize=20)
    await redis.flushall()
    yield redis
    await redis.flushall()
    redis.close()


@pytest.fixture(scope='session')
async def es_client(film_data_prepare):
    elastic_host = f'{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}'
    client = AsyncElasticsearch(hosts=elastic_host)
    etl_loader = ETLLoader(film_data_prepare['index'], client)
    await etl_loader.index_creation(film_data_prepare['index_file'])
    await etl_loader.load_to_es(film_data_prepare['test_data'])
    yield client
    await etl_loader.destroy_es_index()
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(session):
    async def inner(method: str = None, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f'http://{test_settings.SERVICE_HOST}:{test_settings.SERVICE_PORT}/api/v1/{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status, )

    return inner
