from redis import Redis
from os import getenv


REDIS_URI = getenv('REDIS_URI')

_client = Redis.from_url(REDIS_URI)


def get_instance():
    return _client