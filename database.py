import motor.motor_asyncio
from configs import get_configs

client = motor.motor_asyncio.AsyncIOMotorClient(get_configs().mongo_url)
database = client.database
