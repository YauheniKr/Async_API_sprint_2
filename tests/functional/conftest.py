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

PERSON_TEST_DATA = {
    'index': 'person',
    'index_file': SCHEMA_DIR.joinpath('elastic_person_schema.json'),
    'test_data': TESTDATA_DIR.joinpath('person_test_data.json'),
}
FILM_TEST_DATA = {
    'index': 'movies',
    'index_file': SCHEMA_DIR.joinpath('elastic_movies_schema.json'),
    'test_data': TESTDATA_DIR.joinpath('movies_test_data.json'),
}
GENRE_TEST_DATA = {
    'index': 'genre',
    'index_file': SCHEMA_DIR.joinpath('elastic_genre_schema.json'),
    'test_data': TESTDATA_DIR.joinpath('genre_test_data.json'),
}


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((test_settings.REDIS_HOST,
                                              test_settings.REDIS_PORT), minsize=10, maxsize=20)
    await redis.flushall()
    yield redis
    await redis.flushall()
    redis.close()


@pytest.fixture(params=[FILM_TEST_DATA])
async def load_movies_to_es(request, es_client):
    etl_loader = ETLLoader(request.param['index'], es_client)
    await etl_loader.index_creation(request.param['index_file'])
    await etl_loader.load_to_es(request.param['test_data'])
    yield etl_loader
    await etl_loader.destroy_es_index()


@pytest.fixture(params=[PERSON_TEST_DATA])
async def load_person_to_es(request, es_client):
    etl_loader = ETLLoader(request.param['index'], es_client)
    await etl_loader.index_creation(request.param['index_file'])
    await etl_loader.load_to_es(request.param['test_data'])
    yield etl_loader
    await etl_loader.destroy_es_index()


@pytest.fixture(params=[GENRE_TEST_DATA])
async def load_genre_to_es(request, es_client):
    etl_loader = ETLLoader(request.param['index'], es_client)
    await etl_loader.index_creation(request.param['index_file'])
    await etl_loader.load_to_es(request.param['test_data'])
    yield etl_loader
    await etl_loader.destroy_es_index()


@pytest.fixture(scope='session')
async def es_client():
    elastic_host = f'{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}'
    client = AsyncElasticsearch(hosts=elastic_host)
    yield client
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
