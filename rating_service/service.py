import asyncio
import json

import aiocron
from .logic import CalculateRatingService
from coffee.deps import rating_collection
from kafka_producer import producer


async def produce():
    service = CalculateRatingService(rating_collection=rating_collection)
    ratings = await service.calculate_rating()
    async for rating in ratings:
        print(rating)
        await producer.start()
        await producer.send(
            topic='update_ratings_coffee',
            key=b'rating',
            value=json.dumps(rating).encode('utf-8')
        )


@aiocron.crontab('0 23 * * *')
async def compute():
    """calculate rating and update coffee every day at 23:00"""
    await produce()


asyncio.get_event_loop().run_forever()
