from cache_service import CacheServie
from typing import Callable


def cached_coffee(schema_func: Callable, ex: int = 60):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = f'{kwargs}'
            if not (cache := await CacheServie().get_from_cache(key=key)):
                coffee = await func(*args, **kwargs)
                data = await CacheServie().dump_json(coffee)
                await CacheServie().set_to_cache(key=key, value=data, ex=ex)
                return coffee
            return schema_func(cache)

        return wrapper

    return decorator
