from abc import ABC
from typing import Optional

from pydantic import UUID4


class BaseDataStorageService(ABC):
    def __init__(self):
        raise NotImplementedError

    async def get_by_id(self, entity_id):
        raise NotImplementedError


class BaseFilmStorageService(BaseDataStorageService, ABC):
    async def get_film_list(
        self,
        sort: str,
        page_number: int,
        page_size: int,
        filter_genre: str
    ):
        raise NotImplementedError

    async def search_film(
        self,
        query: str,
        page_number: int,
        size: int
    ):
        raise NotImplementedError

    async def get_person_films_by_person_id(self, person_id: UUID4):
        raise NotImplementedError


class BaseGenreStorageService(BaseDataStorageService, ABC):
    async def get_list(self):
        raise NotImplementedError


class BasePersonStorageService(BaseDataStorageService, ABC):
    async def search_person(
        self,
        query: str,
        page_number: int,
        page_size: int
    ):
        raise NotImplementedError


class BaseCacheService:
    async def put_data_to_cache(self, key: str, data: str, expire: int = 20):
        raise NotImplementedError

    async def get_data_from_cache(self, key: str) -> Optional[dict]:
        raise NotImplementedError
