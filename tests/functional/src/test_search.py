import pytest


class TestsSearchApi:

    @pytest.mark.asyncio
    async def test_film_search(self, load_movies_to_es, make_get_request, redis_client):
        param = {'query': 'star wars'}
        response = await make_get_request('film/search', param)
        assert response.status == 200
        assert len(response.body) == 50
        searched_film = {'imdb_rating': 9.5,
                         'title': 'The Secret World of Jeffree Star',
                         'uuid': '05d7341e-e367-4e2e-acf5-4652a8435f93'}
        assert searched_film in response.body

    @pytest.mark.asyncio
    async def test_film_search_custom_param(self, load_movies_to_es, make_get_request, redis_client):
        param = {'query': 'star wars', 'page[number]': 1, 'page[size]': 20}
        response = await make_get_request('film/search', param)
        assert response.status == 200
        assert len(response.body) == 20
        searched_film = {'imdb_rating': 9.5,
                         'title': 'The Secret World of Jeffree Star',
                         'uuid': '05d7341e-e367-4e2e-acf5-4652a8435f93'}
        assert searched_film in response.body

    @pytest.mark.asyncio
    async def test_person_search(self, load_person_to_es, load_movies_to_es, make_get_request, redis_client):
        param = {'query': 'saldana'}
        response = await make_get_request('person/search', param)
        assert response.status == 200
        assert len(response.body) == 1
        assert 'Saldana' in response.body[0]['full_name']
