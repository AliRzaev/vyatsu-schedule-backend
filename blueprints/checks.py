from flask import Blueprint, make_response, jsonify
from pymongo.errors import PyMongoError
from redis import RedisError

from databases import mongo, redis

checks_blueprint = Blueprint('checks', __name__)


@checks_blueprint.route('/health_check')
def health_check():
    return make_response((jsonify(status='OK'), 200))


@checks_blueprint.route('/ready_check')
def ready_check():
    try:
        if not redis.ping():
            return make_response((jsonify(status='Redis is unavailable'), 503))

        if mongo.db is not None:
            mongo.db.command('ismaster')

        return make_response((jsonify(status='Ready'), 200))
    except RedisError:
        return make_response((jsonify(status='Redis is unavailable'), 503))
    except PyMongoError:
        return make_response((jsonify(status='MongoDB is unavailable'), 503))
    except Exception as ex:
        return make_response((jsonify(status=str(ex)), 500))
