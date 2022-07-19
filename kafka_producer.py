import asyncio
from aiokafka import AIOKafkaProducer
from configs import get_configs

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
    bootstrap_servers=get_configs().kafka_host,
    loop=loop,
    linger_ms=2000
)
