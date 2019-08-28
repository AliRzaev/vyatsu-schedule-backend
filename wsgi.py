from os import environ

import config
from server import create_app

if 'FLASK_ENV' not in environ or environ['FLASK_ENV'] == 'development':
    config_obj = config.DevelopmentConfig()
elif environ['FLASK_ENV'] == 'production':
    config_obj = config.ProductionConfig()
elif environ['FLASK_ENV'] == 'testing':
    config_obj = config.TestingConfig()
else:
    raise ValueError("Unknown FLASK_ENV")


app = create_app(config_obj)
