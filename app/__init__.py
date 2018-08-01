# /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask_mongoengine import MongoEngine
from flaskext.markdown import Markdown
from flask_debugtoolbar import DebugToolbarExtension
from config import config

cache = Cache()
mail = Mail()
db = MongoEngine()
login_manager = LoginManager()
debug_tool = DebugToolbarExtension()


def init_app(app):
    """插件初始化"""
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'user.login'

    Markdown(app)
    db.init_app(app)
    mail.init_app(app)
    debug_tool.init_app(app)
    login_manager.init_app(app)


def register_app(app):
    """蓝图注册"""
    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint
    from .user import user as user_blueprint
    from .data import data as data_blueprint
    from .api_v1 import api_v1 as api_v1_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(data_blueprint, url_prefix='/data')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api_v1')

    return app


def create_app(config_name):
    """创建app实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    cache.init_app(app)
    init_app(app)
    app = register_app(app)

    return app
