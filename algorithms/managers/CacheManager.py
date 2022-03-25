import redis

from ..DAO.RedisDao import get_connection
import os


class CacheRepository:
    def __init__(self):
        connection_url = f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_URL')}"
        self.connection = redis.from_url(connection_url)

    # def hset(self, name, key, value=None, mapping=None):
    #     self.connection.hset(name=name, key=key, value=value, mapping=mapping)
    #
    # def hget(self, name, key):
    #     self.connection.hget(name, key)
    #
    # def hexists(self, name, key):
    #     self.connection.hexists(name= name, key= key)

    def __del__(self):
        self.connection.close()
