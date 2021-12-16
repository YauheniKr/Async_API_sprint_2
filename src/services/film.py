from typing import Union
from uuid import UUID

from fastapi import Depends

from src.core.config import settings
from src.db.base_storage import BaseCacheService, BaseFilmStorageService
from src.db.elastic import ElasticMoviesStorageService
from src.db.redis import RedisCacheService
from src.models.film import BaseFilm, FullFilm
from src.services.base_service import BaseService


class FilmService(BaseService):
    def __init__(
        self,
        redis_service: BaseCacheService = Depends(RedisCacheService),
        elastic_service: BaseFilmStorageService = Depends(ElasticMoviesStorageService)
    ):
        self.cache_service = redis_service
        self.data_service = elastic_service

    @BaseService._cache(
        settings.FILM_CACHE_EXPIRE_IN_SECONDS,
        model=BaseFilm
    )
    async def get_film_list(
        self,
        sort: str,
        page_number: str,
        page_size: str,
        filter_genre: UUID
    ) -> Union[list[BaseFilm], None]:

        filter_genre = str(filter_genre) if filter_genre else None
        films = await self.data_service.get_film_list(sort, int(page_number), int(page_size), filter_genre)

        if films:
            films = [BaseFilm(**film) for film in films]

        return films

    @BaseService._cache(
        settings.FILM_CACHE_EXPIRE_IN_SECONDS,
        model=BaseFilm,
    )
    async def search_film(self, query: str, page_number: str, page_size: str) -> Union[list[BaseFilm], None]:
        films = await self.data_service.search_film(query, int(page_number), int(page_size))

        if films:
            films = [BaseFilm(**film) for film in films]

        return films

    @BaseService._cache(
        settings.FILM_CACHE_EXPIRE_IN_SECONDS,
        model=FullFilm,
    )
    async def get_film_by_id(self, film_id):
        film = await self.get_by_id(film_id)
        return FullFilm(**film)

    async def get_person_films_by_person_id(self, person_id):
        return await self.data_service.get_person_films_by_person_id(person_id)
