from flask_redis import FlaskRedis

redis_store = FlaskRedis(decode_responses=True)

KEY_GROUPS = 'groups'

"""Key prefix for date range. The whole key is something like 'group_1234'
"""
KEY_RANGE_PREFIX = 'group_'
