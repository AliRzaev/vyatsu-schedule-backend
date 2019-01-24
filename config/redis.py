from os import getenv

from redis import Redis

REDIS_URI = getenv('REDIS_URL')

_client = Redis.from_url(REDIS_URI, decode_responses=True)


def get_instance():
    return _client


KEY_GROUPS = 'groups'

"""Key prefix for date range. The whole key is something like 'group_1234'
"""
KEY_RANGE_PREFIX = 'group_'
