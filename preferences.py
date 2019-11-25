import os

application_name = 'demography'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = application_name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbuser:dbpassword@127.0.0.1/db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbuser:dbpassword@192.168.0.3/demography_20190826'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbuser:dbpassword@127.0.0.1/demography'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '425BF6E9E8BB1CCCAD5845EFE599B'
    IMPORT_LOG_FILE = 'import.log'
    DEBUG_LOG_FILENAME = 'log.log'
    FIAS_DB = 'fias'
    DEBUG_LOG = True
