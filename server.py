from datetime import datetime
from logging.config import dictConfig
from os import getenv

from flask import Flask, request
from flask_cors import CORS

from blueprints.api_v1 import api_v1_blueprint
from blueprints.api_v2 import api_v2_blueprint
from blueprints.checks import checks_blueprint
from config import redis, mongodb
from utils.prefetch import prefetch

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] '
                      '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z'
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
logger = app.logger

CORS(api_v1_blueprint, methods=['GET'])
CORS(api_v2_blueprint, methods=['GET'])

# Set up Redis
REDIS_URL = getenv('REDIS_URL', '')
if REDIS_URL:
    app.config['REDIS_URL'] = REDIS_URL
    redis.redis_store.init_app(app)
else:
    raise ValueError('REDIS_URL is not defined')

# Set up MongoDB
MONGODB_URI = getenv('MONGODB_URI', '')
if MONGODB_URI:
    app.config['MONGO_URI'] = MONGODB_URI
    mongodb.mongo.init_app(app)


    @api_v1_blueprint.before_request
    @api_v2_blueprint.before_request
    def log():
        mongodb.mongo.db.logs.insert_one({
            'path': request.full_path,
            'useragent': request.user_agent.string,
            'date': datetime.now()
        })

app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')
app.register_blueprint(checks_blueprint)

if __name__ != '__main__':  # logs to console in production environment
    @app.before_request
    def log():
        logger.info('{} {}'.format(request.method, request.full_path))

if __name__ != '__main__':
    logger.info('Prefetching...')

    status = prefetch(redis=redis.redis_store)
    if status[0] is None and status[1] is None:
        logger.info('Prefetch: nothing to do')
    if status[0] is not None:
        logger.info(f'Prefetch: {status[0]} groups')
    if status[1] is not None:
        logger.info(f'Prefetch: {status[1]} departments')

if __name__ == '__main__':
    PORT = getenv('PORT', '80')
    app.run(port=PORT, debug=True)
