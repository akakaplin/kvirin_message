import os
from typing import List
from redis import Redis
from config import Pool


class DB:
    STICKY_SESSIONS_HSET = 'sessions'
    BRIDGE_TO_USERS = 'brideusers'
    USER_KARMA_HSET = 'userkarma'

    def __init__(self, redis, conf: List[Pool]) -> None:
        self.redis = redis
        self.conf = conf
        pass

    def reset_on_startup(self):
        # Remove all sticky sessions
        self.redis.delete(DB.STICKY_SESSIONS_HSET)

        # Delete bridge users
        self.redis.delete(DB.BRIDGE_TO_USERS)

    def get_karma(self, user_id: str):
        return 0

    def bridge_karma_up(self, bridge: str):
        if not self.redis.hexists(DB.USER_KARMA_HSET, bridge):
            self.redis.hincby(DB.USER_KARMA_HSET, bridge, 1)
        else:
            self.redis.hset(DB.USER_KARMA_HSET, bridge, 1)
        return

    def bridge_karma_down(self, bridge: str):
        
        return

    def get_or_set_sticky(self, user_id: str, bridge: str) -> str:
        if self.redis.hexists(DB.STICKY_SESSIONS_HSET, user_id):
            bridge = self.redis.hget(DB.STICKY_SESSIONS_HSET, user_id)
            return bridge.decode()
        else:
            self.redis.hset(DB.STICKY_SESSIONS_HSET, user_id, bridge)
            self.redis.sadd(DB.BRIDGE_TO_USERS, user_id, bridge)
            return bridge


def init_db(conf) -> DB:
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    return DB(r, conf)