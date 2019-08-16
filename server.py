import logging
from datetime import datetime
from os import getenv, environ

from flask import Flask, request
from flask_cors import CORS
from loguru import logger

import databases
from blueprints.api_v1 import api_v1_blueprint
from blueprints.api_v2 import api_v2_blueprint
from blueprints.checks import checks_blueprint
from utils import prefetch

app = Flask(__name__)

# Set up logging
werkzeug = logging.getLogger('werkzeug')
werkzeug.disabled = True
app.logger.disabled = True


@app.after_request
def log(response):
    logger.info(f'{request.method} {request.full_path} {response.status_code}')
    return response


CORS(api_v1_blueprint, methods=['GET'])
CORS(api_v2_blueprint, methods=['GET'])

# Set up Redis
if 'REDIS_URL' in environ:
    app.config['REDIS_URL'] = environ['REDIS_URL']
    databases.redis.init_app(app)
else:
    raise ValueError('REDIS_URL is not defined')

# Set up CLI commands
prefetch.init_app(app)

# Register blueprints
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')
app.register_blueprint(checks_blueprint)

# Set up MongoDB
if 'MONGODB_URI' in environ:
    app.config['MONGO_URI'] = environ['MONGODB_URI']
    databases.mongo.init_app(app)


    @app.after_request
    def log(response):
        databases.mongo.db.logs.insert_one({
            'path': request.full_path,
            'useragent': request.user_agent.string,
            'date': datetime.now(),
            'status': response.status_code
        })

if getenv('FLASK_ENV') == 'production':
    logger.info('Fetching data...')

    with app.app_context():
        status = prefetch.prefetch()
        if status[0] is None and status[1] is None:
            logger.info('Prefetch: nothing to do')
        if status[0] is not None:
            logger.info(f'Prefetch: {status[0]} groups')
        if status[1] is not None:
            logger.info(f'Prefetch: {status[1]} departments')

if __name__ == '__main__':
    PORT = getenv('PORT', '80')
    app.run(port=PORT, debug=True)
