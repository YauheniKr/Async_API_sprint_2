import pytest


class TestsGenreApi:

    @pytest.mark.asyncio
    async def test_genre_detailed(self, redis_client, es_client, film_data_prepare, make_get_request):
        response = await make_get_request('genre/6c162475-c7ed-4461-9184-001ef3d9f26e')
        assert response.status == 200
        assert response.body['uuid'] == '6c162475-c7ed-4461-9184-001ef3d9f26e'
        assert response.body['name'] == 'Sci-Fi'

    @pytest.mark.asyncio
    async def test_genre_list(self, redis_client, es_client, film_data_prepare, make_get_request):
        response = await make_get_request('genre')
        assert response.status == 200
        assert len(response.body) == 26
