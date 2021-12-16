from fastapi import Depends

from src.core.config import settings
from src.db.base_storage import BaseCacheService, BasePersonStorageService
from src.db.elastic import ElasticPersonStorageService
from src.db.redis import RedisCacheService
from src.models.person import Person
from src.services.base_service import BaseService


class PersonService(BaseService):
    namespace = "person"

    def __init__(
        self,
        redis_service: BaseCacheService = Depends(RedisCacheService),
        elastic_service: BasePersonStorageService = Depends(ElasticPersonStorageService),
    ):
        self.cache_service = redis_service
        self.data_service = elastic_service

    @BaseService._cache(
        settings.PERSON_CACHE_EXPIRE_IN_SECONDS,
        model=Person,
    )
    async def get_person_by_id(self, person_id, movies_service) -> Person:
        person = await self.data_service.get_by_id(person_id)
        films = await movies_service.get_person_films_by_person_id(person_id)

        film_ids = [film["id"] for film in films]
        return Person(**person, film_ids=film_ids)

    @BaseService._cache(
        settings.PERSON_CACHE_EXPIRE_IN_SECONDS,
        model=Person,
    )
    async def search_person(
        self, query: str, page_number: int, page_size: int, movies_service
    ) -> list[Person]:
        persons = await self.data_service.search_person(
            query=query,
            page_number=page_number,
            page_size=page_size,
        )

        out_persons = list()
        for p in persons:
            films = await movies_service.get_person_films_by_person_id(p["id"])
            film_ids = [f["id"] for f in films]
            person = Person(**p, film_ids=film_ids)
            out_persons.append(person)

        return out_persons
