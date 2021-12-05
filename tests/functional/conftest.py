import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import SERVICE_URL, ELASTIC_HOST
from tests.functional.utils.models import HTTPResponse


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=ELASTIC_HOST)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str = None, params: dict = None) -> HTTPResponse:
        params = params or {}
        # url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        url = f'{SERVICE_URL}/api/v1/film/{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status,)

    return inner
