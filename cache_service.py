import json
from typing import Union
import aioredis


class CacheServie:
    def __init__(self):
        self.aio_redis = aioredis.from_url(
            "redis://localhost", decode_responses=True
        )

    async def set_to_cache(
            self, key: str, value: Union[str, bytes, int, float], ex: int = 60
    ):
        await self.aio_redis.set(name=key, value=value, ex=ex)

    async def get_from_cache(self, key: str):
        return await self.aio_redis.get(name=key)

    @staticmethod
    async def dump_json(obj) -> bytes:
        return json.dumps(obj, indent=4, sort_keys=True, default=str) \
            .encode('utf-8')
