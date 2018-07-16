from os import getenv

from flask import Flask, request
from flask_cors import CORS

from blueprints.api_v1 import api_v1_blueprint
from blueprints.api_v2 import api_v2_blueprint

from models import logs

PORT = getenv('PORT', '8080')

app = Flask(__name__)


CORS(api_v1_blueprint, methods=['GET'])
CORS(api_v2_blueprint, methods=['GET'])

app.register_blueprint(api_v1_blueprint, url_prefix='/vyatsu')  # backward compatibility
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

app.register_blueprint(api_v2_blueprint, url_prefix='/vyatsu/v2')  # backward compatibility
app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')


@app.before_request
def logs_to_mongo():  # logs each request into MongoDB
    logs.insert_one(request.full_path)


if __name__ == '__main__':
    app.run(port=PORT, debug=True)
