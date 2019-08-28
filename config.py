from os import environ


class Config:
    DEBUG = False
    TESTING = False
    REDIS_URL = 'redis://localhost:6379/0'
    PDF2JSON_API_URL = 'http://localhost:8080'

    def __init__(self):
        if 'MONGODB_URI' in environ:
            self.MONGO_URI = environ['MONGODB_URI']


class ProductionConfig(Config):

    def __init__(self):
        super().__init__()

        self.REDIS_URL = environ['REDIS_URL']
        self.PDF2JSON_API_URL = environ['PDF2JSON_API_URL']


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
