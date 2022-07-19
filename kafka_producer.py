from aiokafka import AIOKafkaProducer
from configs import get_configs


async def create_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=get_configs().kafka_host,
        linger_ms=2000
    )
    return producer
