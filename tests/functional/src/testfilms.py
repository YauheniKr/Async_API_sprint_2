import pytest

from tests.functional.settings import TESTDATA_DIR, SCHEMA_DIR
from tests.functional.utils.etl_loader import ETLLoader


class TestsFilmsApi:

    @pytest.mark.asyncio
    async def test_film_detailed(self, es_client, make_get_request): #Todo: вынести в Abstract class
        etl_loader = ETLLoader('movies', es_client)
        index_file = SCHEMA_DIR.joinpath('elastic_movies_schema.json')
        await etl_loader.index_creation(index_file)
        test_data_filepath = TESTDATA_DIR.joinpath('movies_test_data.json')
        await etl_loader.load_to_es(test_data_filepath)

        response = await make_get_request('00af52ec-9345-4d66-adbe-50eb917f463a')

        # Проверка результата
        assert response.status == 200
        assert response.body['uuid'] == '00af52ec-9345-4d66-adbe-50eb917f463a'
        # assert len(response.body) == 1

        # assert response.body == expected
