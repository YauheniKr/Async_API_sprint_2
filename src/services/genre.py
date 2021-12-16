import elasticsearch
from elasticsearch_dsl import Search
from fastapi import Depends

from src.core.config import settings
from src.db.base_storage import BaseCacheService, BaseGenreStorageService
from src.db.elastic import ElasticGenreStorageService
from src.db.redis import RedisCacheService
from src.models.genre import Genre
from src.services.base_service import BaseService


class GenreService(BaseService):
    def __init__(
        self,
        redis_service: BaseCacheService = Depends(RedisCacheService),
        elastic_service: BaseGenreStorageService = Depends(ElasticGenreStorageService)
    ):
        self.cache_service = redis_service
        self.data_service = elastic_service

    @BaseService._cache(
        settings.GENRE_CACHE_EXPIRE_IN_SECONDS,
        model=Genre,
    )
    async def get_genre_by_id(self, genre_id):
        genre = await self.data_service.get_by_id(genre_id)
        return Genre(**genre)

    @BaseService._cache(
        settings.GENRE_CACHE_EXPIRE_IN_SECONDS,
        model=Genre,
    )
    async def get_genre_list(self):
        try:
            genres = await self.data_service.get_list()
        except elasticsearch.exceptions.NotFoundError:
            return None
        return [Genre(**g) for g in genres]
