import pytest

from tests.functional.settings import SCHEMA_DIR, TESTDATA_DIR


class TestsGenreApi:
    GENRE_TEST_DATA = {
        'index': 'genre',
        'index_file': SCHEMA_DIR.joinpath('elastic_genre_schema.json'),
        'test_data': TESTDATA_DIR.joinpath('genre_test_data.json'),
    }

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [GENRE_TEST_DATA], indirect=True)
    async def test_genre_detailed(self, es_client, make_get_request):
        response = await make_get_request('genre/6c162475-c7ed-4461-9184-001ef3d9f26e')
        assert response.status == 200
        assert response.body['uuid'] == '6c162475-c7ed-4461-9184-001ef3d9f26e'
        assert response.body['name'] == 'Sci-Fi'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [GENRE_TEST_DATA], indirect=True)
    async def test_genre_list(self, es_client, make_get_request):
        response = await make_get_request('genre')
        assert response.status == 200
        assert len(response.body) == 26

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [GENRE_TEST_DATA], indirect=True)
    async def test_genre_list_empty(self, redis_client, es_client, make_get_request):
        await redis_client.flushall()
        await es_client.indices.delete(self.GENRE_TEST_DATA['index'])
        response = await make_get_request('genre')
        assert response.status == 200
        assert len(response.body) == 0
        assert response.body == []