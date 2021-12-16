from http import HTTPStatus

import pytest

from tests.functional.conftest import GENRE_TEST_DATA, load_movies_to_es


class TestsGenreApi:

    @pytest.mark.asyncio
    async def test_genre_detailed(self, load_genre_to_es, redis_client, make_get_request):
        test_data = load_genre_to_es._get_json_data(GENRE_TEST_DATA['test_data'])[0]
        test_id = test_data['id']
        response = await make_get_request(f'genre/{test_id}')
        assert response.status == HTTPStatus.OK
        assert response.body['uuid'] == test_data['id']
        assert response.body['name'] == test_data['name']

    @pytest.mark.asyncio
    async def test_genre_list(self, load_genre_to_es, redis_client, make_get_request):
        response = await make_get_request('genre')
        tests_data = load_genre_to_es._get_json_data(GENRE_TEST_DATA['test_data'])
        tests_data = [{'uuid': test_data['id'], 'name': test_data['name']} for test_data in tests_data]
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 26
        assert response.body == tests_data

    @pytest.mark.asyncio
    async def test_genre_list_empty(self, redis_client, make_get_request):
        await redis_client.flushall()
        response = await make_get_request('genre')
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 0
        assert response.body == []
