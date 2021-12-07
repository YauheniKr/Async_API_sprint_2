import pytest

#from tests.functional.conftest import make_get_request, film_data_prepare
#from tests.functional.settings import TESTDATA_DIR, SCHEMA_DIR
#from tests.functional.utils.etl_loader import ETLLoader


class TestsFilmsApi:

    @pytest.mark.asyncio
    async def test_film_detailed(self, film_data_prepare, make_get_request): #Todo: вынести в Abstract class
        response = await make_get_request('00af52ec-9345-4d66-adbe-50eb917f463a')
        assert response.status == 200
        assert response.body['uuid'] == '00af52ec-9345-4d66-adbe-50eb917f463a'

    @pytest.mark.asyncio
    async def test_film_list(self, film_data_prepare, make_get_request):
        response = await make_get_request('?sort=-imdb_rating')
        assert response.status == 200

        assert len(response.body) == 4
