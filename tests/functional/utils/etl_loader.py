import json
import logging

from elasticsearch import AsyncElasticsearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLLoader:
    def __init__(self, index_name: str, es_client: AsyncElasticsearch):
        self.index_name = index_name
        self.es_client = es_client

    def _get_json_data(self, json_file: str) -> list[json]:
        """
        МЕтод для получения json данных из файла
        :param json_file: имя файла с данными
        :return: список json
        """
        with open(json_file) as file:
            scheme_dict = json.load(file)
        return scheme_dict

    async def index_creation(self) -> None:
        """
        Проверяем и создаем индекс
        """
        index_exist = await self.es_client.indices.exists(self.index_name)
        scheme_dict = self._get_json_data('/tests/functional/utils/elastic_movies_schema.json')
        if not index_exist:
            await self.es_client.indices.create(index=self.index_name, body=scheme_dict)

    def _get_es_bulk_query(self, rows: list[dict]) -> list[str]:
        """
        Подготавливает bulk-запрос в Elasticsearch
        :param rows: Список словарей с данными
        :return: Список строк подготовленный для загрузки
        """
        prepared_query = []
        for row in rows:
            prepared_query.extend([json.dumps({'index': {'_index': self.index_name,
                                                         '_id': row['id']}}), json.dumps(row)])
        return prepared_query

    async def load_to_es(self, file_data_name: str) -> None:
        """
        Отправка запроса в ES и разбор ошибок сохранения данных
        file_data_name: имя файла с данными для заливки в Elasticsearch
        :return: None
        """
        json_data = self._get_json_data(file_data_name)
        prepared_query = self._get_es_bulk_query(json_data)
        adopted_query = '\n'.join(prepared_query) + '\n'
        response = await self.es_client.bulk(adopted_query)

        for item in response['items']:
            error_message = item['index'].get('error')
            if error_message:
                logger.error(error_message)
        await self.es_client.close()
