import asyncio
import json

from aiokafka import AIOKafkaConsumer
from bson import ObjectId

from .deps import coffee_collection
from configs import get_configs
from pymongo import UpdateOne


async def __update_rating(coffee_id: str, avg_rating: float):
    requests = [
        UpdateOne(
            filter={'_id': ObjectId(coffee_id)},
            update={'$set': {'rating': avg_rating}}
        )
    ]
    _ = await coffee_collection.bulk_write(requests=requests)


async def consume_rating():
    consumer = AIOKafkaConsumer(
        'update_ratings_coffee',
        bootstrap_servers=get_configs().kafka_host,
        group_id='update-rating-group',
    )
    await consumer.start()
    async for msg in consumer:
        data = json.loads(msg.value)
        await __update_rating(
            coffee_id=data['coffee_id'],
            avg_rating=data['avg_rating']
        )


if __name__ == '__main__':
    asyncio.run(consume_rating())
