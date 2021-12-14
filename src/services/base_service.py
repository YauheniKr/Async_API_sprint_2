import json
from typing import Optional

from pydantic import BaseModel, parse_obj_as

from src.db.base_storage import BaseDataStorageService, BaseCacheService


class BaseService:
    def __init__(
        self,
        redis: BaseCacheService,
        elastic: BaseDataStorageService
    ):
        self.data_service = elastic
        self.cache_service = redis

    async def get_by_id(self, entity_id) -> Optional[dict]:
        entity = await self.data_service.get_by_id(entity_id=entity_id)
        return entity

    def _cache(expiration_time, model):
        def decorator(fn):
            async def inner(self, *args, **kwargs):
                cache_key = self.get_cache_key(fn, *args, **kwargs)
                obj: dict = await self.search_in_cache(cache_key)
                if not obj:
                    obj: BaseModel = await fn(self, *args, **kwargs)
                    if isinstance(obj, BaseModel):
                        await self.put_to_cache(
                            key=cache_key, value=obj.json(), expire=expiration_time
                        )
                    elif isinstance(obj, list):
                        await self.put_to_cache(json.dumps([o.json() for o in obj]), cache_key, expiration_time)
                else:
                    obj = parse_obj_as(model, obj)
                return obj

            return inner

        return decorator

    _cache = staticmethod(_cache)

    async def search_in_cache(self, key: str):
        return await self.cache_service.get_data_from_cache(key)

    async def put_to_cache(self, key: str, value: dict, expire: int):
        return await self.cache_service.put_data_to_cache(key=key, data=value, expire=expire)

    def get_cache_key(self, fn, *args, **kwargs):
        ordered_kwargs = sorted(kwargs.items())
        return (
            (fn.__module__ or "")
            + "."
            + fn.__name__
            + str(args)
            + str(ordered_kwargs)
        )
