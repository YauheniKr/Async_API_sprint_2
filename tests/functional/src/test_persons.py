from http import HTTPStatus

import pytest

from tests.functional.conftest import PERSON_TEST_DATA, FILM_TEST_DATA, prepare_person_film_data


class TestsPersonApi:

    @pytest.mark.asyncio
    async def test_person_detailed(self, load_person_to_es, load_movies_to_es,
                                   redis_client, make_get_request):
        test_person_data = load_person_to_es._get_json_data(PERSON_TEST_DATA['test_data'])[0]
        test_data_id = test_person_data['id']
        response = await make_get_request(f'person/{test_data_id}')
        assert response.status == HTTPStatus.OK
        assert response.body['uuid'] == test_data_id
        assert response.body['full_name'] == test_person_data['full_name']
        assert response.body['role'] == test_person_data['role']

    @pytest.mark.asyncio
    async def test_person_films(self, load_person_to_es, load_movies_to_es, redis_client, make_get_request):
        test_person_data = load_person_to_es._get_json_data(PERSON_TEST_DATA['test_data'])[0]
        test_movies_data = load_movies_to_es._get_json_data(FILM_TEST_DATA['test_data'])
        test_data_id = test_person_data['id']
        test_data_dict = {'id': test_person_data['id'], 'name': test_person_data['full_name']}
        test_film_person_data = prepare_person_film_data(test_data_dict, test_movies_data)
        response = await make_get_request(f'person/{test_data_id}/film')
        assert response.status == HTTPStatus.OK
        assert response.body == test_film_person_data
