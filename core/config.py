import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_user = os.getenv('DATABASE_USERNAME', 'foo')
db_pass = os.getenv('DATABASE_PASSWORD', 'bar')
db_name = os.getenv('DATABASE_NAME', 'test')
db_server = os.getenv('DATABASE_SERVER', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')
db_type = os.getenv('DATABASE_TYPE', 'postgres')
db_url = f"{db_type}://{db_user}:{db_pass}@{db_server}:{db_port}/{db_name}"
secret_key = os.getenv("SECRET_KEY", b'\xe3\x99\x001~\x0fgDY\x97{)<6\x17p')


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secret_key


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
