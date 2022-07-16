from cache_service import CacheServie
from .schemas import CoffeeSchema


def cache_detail_coffee(ex: int = 60):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = f'{kwargs["coffee_id"]}'
            if not (cache := await CacheServie().get_from_cache(key=key)):
                coffee = await func(*args, **kwargs)
                data = await CacheServie().dump_json(coffee)
                await CacheServie().set_to_cache(key=key, value=data, ex=ex)
                return coffee
            return CoffeeSchema.from_obj(cache)

        return wrapper

    return decorator


def cache_coffees(ex: int = 60):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = f'{kwargs["limit"]}-{kwargs["skip"]}'
            if not (cache := await CacheServie().get_from_cache(key=key)):
                coffee = await func(*args, **kwargs)
                data = await CacheServie().dump_json(coffee)
                await CacheServie().set_to_cache(key=key, value=data, ex=ex)
                return coffee
            return CoffeeSchema.from_list(cache)

        return wrapper

    return decorator
