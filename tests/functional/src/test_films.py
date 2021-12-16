from http import HTTPStatus

import pytest

from tests.functional.conftest import FILM_TEST_DATA, adopt_test_data_movies, adopt_film_list_data


class TestsFilmsApi:

    @pytest.mark.asyncio
    async def test_film_detailed(self, load_movies_to_es, make_get_request, redis_client):
        test_data = load_movies_to_es._get_json_data(FILM_TEST_DATA['test_data'])[0]
        test_data_id = test_data['id']
        response = await make_get_request(f'film/{test_data_id}')
        test_data = adopt_test_data_movies(test_data)
        assert response.status == HTTPStatus.OK
        assert response.body == test_data

    @pytest.mark.asyncio
    async def test_film_list(self, load_movies_to_es, make_get_request):
        response = await make_get_request('film?sort=-imdb_rating')
        tests_data = load_movies_to_es._get_json_data(FILM_TEST_DATA['test_data'])
        tests_data = adopt_film_list_data(tests_data)
        assert response.status == HTTPStatus.OK
        sorted_test_data = sorted(tests_data, key=lambda x: -x['imdb_rating'])
        assert response.body == sorted_test_data[:50]
        assert len(response.body) == 50

    @pytest.mark.asyncio
    async def test_film_list_custom_pagination(self, load_movies_to_es, make_get_request):
        response = await make_get_request('film', params={'sort': '-imdb_rating', 'page[size]': 20, 'page[number]': 1})
        tests_data = load_movies_to_es._get_json_data(FILM_TEST_DATA['test_data'])
        tests_data = adopt_film_list_data(tests_data)
        sorted_test_data = sorted(tests_data, key=lambda x: -x['imdb_rating'])
        assert response.status == HTTPStatus.OK
        assert response.body == sorted_test_data[:20]
        assert len(response.body) == 20

    @pytest.mark.asyncio
    async def test_film_list_filter(self, load_movies_to_es, make_get_request):
        genre_data = {
            'id': "1cacff68-643e-4ddd-8f57-84b62538081a",
            'name': "Drama"
        }
        response = await make_get_request('film',
                                          params={'sort': '-imdb_rating', 'page[size]': 20, 'page[number]': 1,
                                                  'filter[genre]': genre_data['id']})
        assert response.status == HTTPStatus.OK
        tests_data = load_movies_to_es._get_json_data(FILM_TEST_DATA['test_data'])
        out = []
        for data in tests_data:
            if genre_data in data['genre']:
                out.append(data)
        out_tests = adopt_film_list_data(out)
        assert response.body == sorted(out_tests, key=lambda x: -x['imdb_rating'])
