import os
from redis import Redis
from config import Config


class DB:
    def __init__(self, redis) -> None:
        self.redis = redis
        pass

    def reset_on_startup():
        return


def init_db(config: Config) -> DB:
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    return Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)