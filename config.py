# /usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'

    _BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__name__)))

    MONGODB_CONNECT = True

    SAVEPIC = os.path.join(_BASE_DIR, 'app/static/img').replace('\\', '/')

    POST_IMG_URL = os.path.join(
        _BASE_DIR, 'app/static/postImg').replace("\\", '/')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


    # pagination page
    FLASKY_POSTS_PER_PAGE = 3

    # pyecharts js
    # REMOTE_HOST = "https://pyecharts.github.io/assets/js"

    # email config
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PASSWORD = 'djpxlkwlcikcbaad'
    MAIL_USERNAME = '1285590084@qq.com'
    MAIL_DEFAULT_SENDER = "1285590084@qq.com"

    # redis config
    CACHE_TYPE = 'redis'
    REDIS = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': '0',
        'CACHE_REDIS_PASSWORD': ''
    }


class DevConfig(Config):
    DEBUG = True

    # mongodb config
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/flyDB', 'connect': True}


class ProConfig(Config):
    DEBUG = False
    MONGO_DB = 'flydb'
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/{}'.format(MONGO_DB),
        'connect': True
    }


config = {'development': DevConfig,
          'production': ProConfig,
          'default': DevConfig}
