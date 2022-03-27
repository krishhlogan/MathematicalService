import redis


def get_connection(connection_url):
    return redis.from_url(connection_url)
