from http import HTTPStatus

import pytest


class TestsGenreApi:

    @pytest.mark.asyncio
    async def test_genre_detailed(self, load_genre_to_es, redis_client, make_get_request):
        response = await make_get_request('genre/6c162475-c7ed-4461-9184-001ef3d9f26e')
        assert response.status == HTTPStatus.OK
        assert response.body['uuid'] == '6c162475-c7ed-4461-9184-001ef3d9f26e'
        assert response.body['name'] == 'Sci-Fi'

    @pytest.mark.asyncio
    async def test_genre_list(self, load_genre_to_es, redis_client, make_get_request):
        response = await make_get_request('genre')
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 26

    @pytest.mark.asyncio
    async def test_genre_list_empty(self, redis_client, make_get_request):
        await redis_client.flushall()
        response = await make_get_request('genre')
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 0
        assert response.body == []
