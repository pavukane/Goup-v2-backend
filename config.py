from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv('.flaskenv')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ["MYSQL_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["SECRET_KEY"]

    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


 