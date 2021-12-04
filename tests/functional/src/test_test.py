import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.etl_loader import ETLLoader

SERVICE_URL = 'http://127.0.0.1:8000'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
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
        url = 'http://192.168.88.131:8000/api/v1/film/00af52ec-9345-4d66-adbe-50eb917f463a'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):

    etl_loader = ETLLoader('movies', es_client)
    await etl_loader.index_creation()
    await etl_loader.load_to_es('/tests/functional/utils/movies_test_data.json')

    # Выполнение запроса
    response = await make_get_request()

    # Проверка результата
    assert response.status == 200
    #assert len(response.body) == 1

    # assert response.body == expected
