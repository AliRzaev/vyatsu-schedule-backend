from flask_redis import FlaskRedis

redis_store = FlaskRedis(decode_responses=True)

KEY_GROUPS = 'groups'

KEY_DEPARTMENTS = 'departments'

KEY_RANGE_PREFIX = 'group_'
"""
Key prefix for group's date range. The whole key is something like 'group_1234'
"""

KEY_DEPARTMENT_RANGE_PREFIX = 'department_'
"""
Key prefix for department's date range.
The whole key is something like 'department_1234'
"""
