import pytest

from tests.functional.settings import SCHEMA_DIR, TESTDATA_DIR


class TestsFilmsApi:
    FILM_TEST_DATA = {
        'index': 'movies',
        'index_file': SCHEMA_DIR.joinpath('elastic_movies_schema.json'),
        'test_data': TESTDATA_DIR.joinpath('movies_test_data.json'),
    }

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [FILM_TEST_DATA], indirect=True)
    async def test_film_detailed(self, es_client, make_get_request):
        response = await make_get_request('film/00af52ec-9345-4d66-adbe-50eb917f463a')
        assert response.status == 200
        assert response.body['uuid'] == '00af52ec-9345-4d66-adbe-50eb917f463a'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [FILM_TEST_DATA], indirect=True)
    async def test_film_list(self, es_client, make_get_request):
        response = await make_get_request('film?sort=-imdb_rating')
        assert response.status == 200
        assert response.body == sorted(response.body, key=lambda x: -x['imdb_rating'])
        assert len(response.body) == 50

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [FILM_TEST_DATA], indirect=True)
    async def test_film_list_custom_pagination(self, es_client, make_get_request):
        response = await make_get_request('film', params={'sort': '-imdb_rating', 'page[size]': 20, 'page[number]': 1})
        assert response.status == 200
        assert response.body == sorted(response.body, key=lambda x: -x['imdb_rating'])
        assert len(response.body) == 20

    @pytest.mark.asyncio
    @pytest.mark.parametrize('es_client', [FILM_TEST_DATA], indirect=True)
    async def test_film_list_filter(self, es_client, make_get_request):
        response = await make_get_request('film',
                                          params={'sort': '-imdb_rating', 'page[size]': 20, 'page[number]': 1,
                                                  'filter[genre]': '1cacff68-643e-4ddd-8f57-84b62538081a'})
        assert response.status == 200
        assert response.body == sorted(response.body, key=lambda x: -x['imdb_rating'])
        assert len(response.body) == 10
