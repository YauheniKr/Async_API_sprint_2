import json
from typing import Optional

from aioredis import Redis
from fastapi import Depends

from src.db.base_storage import BaseCacheService

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


class RedisCacheService(BaseCacheService):
    def __init__(self, redis_client: Redis = Depends(get_redis)):
        self.redis_client = redis_client

    async def put_data_to_cache(self, key: str, data: str, expire: int = 20):
        await self.redis_client.set(key=key, value=data, expire=expire)

    async def get_data_from_cache(self, s_key: str) -> Optional[dict]:
        data = await self.redis_client.get(s_key)
        if not data:
            return None
        data = json.loads(data)
        return data
