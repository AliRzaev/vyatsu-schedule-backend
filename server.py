from os import getenv

from flask import Flask
from flask_cors import CORS

from utils.wrappers import on_exception
from blueprints.api_v1 import api_v1_blueprint
from blueprints.api_v2 import api_v2_blueprint

PORT = getenv('PORT', '8080')
IP = getenv('IP', '0.0.0.0')

app = Flask(__name__)


# For testing
@app.route('/test', methods=['GET'])
@on_exception(500)
def get_test():
    return 'OK'


CORS(api_v1_blueprint, methods=['GET'])
CORS(api_v2_blueprint, methods=['GET'])

app.register_blueprint(api_v1_blueprint, url_prefix='/vyatsu')  # backward compatibility
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

app.register_blueprint(api_v2_blueprint, url_prefix='/vyatsu/v2')  # backward compatibility
app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')


if __name__ == '__main__':
    app.run(IP, PORT, debug=True)
