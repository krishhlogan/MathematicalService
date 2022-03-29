import redis

import os


class CacheRepository:
    def __init__(self):
        connection_url = f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_URL')}:{os.environ.get('REDIS_PORT')}"
        self.connection = redis.from_url(connection_url)

    def hset(self, name, key, value=None, mapping=None):
        return self.connection.hset(name=name, key=key, value=value, mapping=mapping)

    def hget(self, name, key):
        return self.connection.hget(name, key)

    def hexists(self, name, key):
        return self.connection.hexists(name=name, key=key)

    def hkeys(self, name, natural_sort=False):
        keys = self.connection.hkeys(name=name)
        return sorted(keys, key=lambda x: int(x)) if natural_sort else keys

    def __del__(self):
        self.connection.close()
