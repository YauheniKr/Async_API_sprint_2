from http import HTTPStatus

import pytest


class TestsPersonApi:

    @pytest.mark.asyncio
    async def test_person_detailed(self, load_person_to_es, load_movies_to_es,
                                   redis_client, make_get_request):
        response = await make_get_request('person/26e83050-29ef-4163-a99d-b546cac208f8')
        assert response.status == HTTPStatus.OK
        assert response.body == {
            "uuid": "26e83050-29ef-4163-a99d-b546cac208f8",
            "full_name": "Mark Hamill",
            "role": [
                "actor",
                "director"
            ],
            'film_ids': ['025c58cd-1b7e-43be-9ffb-8571a613579b',
                         '0312ed51-8833-413f-bff5-0e139c11264a']
        }

    @pytest.mark.asyncio
    async def test_person_films(self, load_person_to_es, load_movies_to_es, redis_client, make_get_request):
        response = await make_get_request('person/26e83050-29ef-4163-a99d-b546cac208f8/film')
        assert response.status == HTTPStatus.OK
        assert response.body == [
            {'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
             'imdb_rating': 8.3,
             'title': 'Star Wars: Episode VI - Return of the Jedi'},
            {'id': '0312ed51-8833-413f-bff5-0e139c11264a',
             'imdb_rating': 8.7,
             'title': 'Star Wars: Episode V - The Empire Strikes Back'},
        ]
