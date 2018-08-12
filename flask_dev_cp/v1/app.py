
import logging
from flask import Flask
from flask_cors import CORS
from routes import docs
from werkzeug.utils import import_string
from flask_mongoengine import MongoEngine
blueprints = ['routes:uploadApi']


# 初始化app
def create_app(app_name='HOMEWORK_API'):
    app = Flask(app_name)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # 自定义错误日志
    handler = logging.FileHandler('app.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    db = MongoEngine()
    # 注册所有蓝图
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    # 跨域
    CORS(app, supports_credentials=True)
    db.init_app(app)
    docs.init_app(app)
    return app
