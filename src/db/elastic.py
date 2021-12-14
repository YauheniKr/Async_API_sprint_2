from typing import Optional

import elasticsearch
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Search, Q
from fastapi import Depends
from pydantic import UUID4

from src.db.base_storage import BaseFilmStorageService, BaseGenreStorageService, BasePersonStorageService

es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    return es


def get_pagination_param(page_number: int, size: int) -> tuple:
    start_number = (page_number - 1) * size
    end_number = page_number * size
    return start_number, end_number


class ElasticMoviesStorageService(BaseFilmStorageService):
    index = 'movies'

    def __init__(self, client: AsyncElasticsearch = Depends(get_elastic)):
        self.es_client = client

    async def get_by_id(self, entity_id):
        s = Search(index=self.index).query("match", id=entity_id)
        doc = await self.es_client.search(index=self.index, body=s.to_dict())
        entity = doc['hits']['hits']

        if entity is None:
            return None
        entity = entity[0]['_source']
        return entity

    async def get_film_list(
        self,
        sort: str,
        page_number: int,
        page_size: int,
        filter_genre: str
    ):
        start_number, end_number = get_pagination_param(page_number, page_size)

        s = Search(index=self.index).query("match_all").sort(sort)[start_number:end_number]
        if filter_genre:
            s = Search(index="movies").query("bool", minimum_should_match=1, should=[
                Q("nested", path="genre", query=Q("match", genre__id=str(filter_genre)))
            ]).sort(sort)[start_number:end_number]
        doc = await self.es_client.search(index=self.index, body=s.to_dict())
        films = doc['hits']['hits']
        if films is None:
            return None

        films = [film['_source'] for film in films]

        return films

    async def search_film(
        self,
        query: str,
        page_number: int,
        size: int
    ):
        start_number, end_number = get_pagination_param(page_number, size)
        s = Search(index=self.index).query("multi_match", query=query, fuzziness="auto")[start_number:end_number]

        try:
            doc = await self.es_client.search(index=self.index, body=s.to_dict())
            films = doc['hits']['hits']
        except elasticsearch.exceptions.NotFoundError:
            films = None

        if films is not None:
            films = [film['_source'] for film in films]

        return films

    async def get_person_films_by_person_id(self, person_id: UUID4):
        search_query = Search(index=self.index).query("bool", minimum_should_match=1, should=[
            Q("nested", path="actors", query=Q("match", actors__id=str(person_id))),
            Q("nested", path="writers", query=Q("match", writers__id=str(person_id))),
            Q("nested", path="directors", query=Q("match", directors__id=str(person_id))),
        ])
        films_from_elastic = await self.es_client.search(index=self.index, body=search_query.to_dict())
        return [film["_source"] for film in films_from_elastic["hits"]["hits"]]


class ElasticGenreStorageService(BaseGenreStorageService):
    index = 'genre'

    def __init__(self, client: AsyncElasticsearch = Depends(get_elastic)):
        self.es_client = client

    async def get_by_id(self, entity_id):
        s = Search(index=self.index).query("match", id=entity_id)
        try:
            doc = await self.es_client.search(index=self.index, body=s.to_dict())
            genre = doc['hits']['hits']
        except elasticsearch.exceptions.NotFoundError:
            genre = None
        if genre is None:
            return None

        entity = genre[0]['_source']
        return entity

    async def get_list(self):
        s = Search(index=self.index).query("match_all")[:1000]

        doc = await self.es_client.search(index=self.index, body=s.to_dict())
        genres = doc['hits']['hits']
        if genres is None:
            return None

        if genres is not None:
            genres = [genre['_source'] for genre in genres]

        return genres


class ElasticPersonStorageService(BasePersonStorageService):
    index = 'person'

    def __init__(self, client: AsyncElasticsearch = Depends(get_elastic)):
        self.es_client = client

    async def get_by_id(self, entity_id):
        s = Search(index=self.index).query("ids", values=[entity_id])
        doc = await self.es_client.search(index=self.index, body=s.to_dict())
        entity = doc['hits']['hits']

        if entity is None:
            return None
        entity = entity[0]['_source']
        return entity

    async def search_person(self, query: str, page_number: int, page_size: int):
        start_number, end_number = get_pagination_param(int(page_number), int(page_size))
        s = (
            Search(index=self.index).query("multi_match", query=query, fuzziness="auto")[start_number:end_number]
        )
        doc = await self.es_client.search(index=self.index, body=s.to_dict())

        persons = doc['hits']['hits']

        if persons is None:
            return None

        persons = [person['_source'] for person in persons]

        return persons
