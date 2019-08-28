from flask_pymongo import PyMongo
from flask_redis import FlaskRedis

mongo = PyMongo()
redis = FlaskRedis(decode_responses=True)
