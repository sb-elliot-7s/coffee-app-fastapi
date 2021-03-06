from pydantic import BaseSettings


class Configs(BaseSettings):
    mongo_url: str

    secret_key: str

    algorithm: str
    exp_time: int

    test: bool
    host: str
    kafka_host: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs():
    return Configs()
