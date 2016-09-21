# app/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = 'my_precious'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 12
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@localhost:3306/logintry'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
