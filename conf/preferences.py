import os

application_name = 'demography'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = application_name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbuser:dbpassword@localhost/demography'
    SQLALCHEMY_POOL_TIMEOUT = 600
    SQLALCHEMY_POOL_RECYCLE = 300
    SQLALCHEMY_POOL_PRE_PING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '425BF6E9E8BB1CCCAD5845EFE599B'
    DEBUG_LOG = True
    DEBUG_LOG_FILENAME = '/var/log/demography/log.log'
    FIAS_DB = 'fias'
