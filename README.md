# Flask+mongo探讨

最近遇到了很多问题，快速总结下问题以及已经解决的部分，大家可以一块交流探讨

### 技术框架

- Flask
- pymongo
- mongoengine
- flask-restful
- Logging
- 新增flask-admin

### 项目模块拆分

------

> 原则上是拆的越细越好，各模块之间功能分离，易于维护，可指派task给团队成员，各人维护不同模块

- 主入口`manage.py`
- 初始化`__init__.py`， 各个应用在此注册，如蓝图，logging，db等
- 路由`routes.py`，蓝图在此实例化，api所有接口放在这里方便查看管理 
- `utli` 自己封装的外部方法，哪个应用需要就调用
- `api` 下面不同的数据库就建不同应用，应用包含`models.py`和`api.py`
- `admin` 作为可视化后台模型视图管理界面，目前实现了模型视图可视化，还未添加flask-login校验

### 已解决问题

------

1.循环调用问题，模块拆分可使项目更加清晰，但模块间难免有调用的情况，但如果a调用b,b又调用a，就会造成循环调用，报错.  建议重头梳理项目关系，避免循环调用

2.mongoengine, mongo最大的特点就是其自由度,易扩展，建表时不需要id字段，mongo会自己添加一个`_id`字段，取的时候就是`obj.id`或者`obj['id']`，如果表中既有id字段又有`_id`字段，那就取不到`id`字段了，解决方法是：model中collections下，

```
class Lessons(Document):
    """课时"""
    uid = StringField(db_field='id')
    num = StringField()
    level = StringField()
```

采取映射，使用`db_field`将uid字段映射到数据库表中的id字段，取值时

```python
lesson = Lesson.objects.first()
lesson.uid
```

3.restful跨域问题，跨域问题在前后端交互算是很经典的问题了，理论上就是`Access-Control-Allow-Origin`设置为*，请求头allow参数开放，可以在`__init__.py`文件中设置全局请求头

```python
# 全局响应头
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response
```

然后

```
pip install Flask-Cors
# 在__init__.py中的createapp方法中注册
CORS(app, supports_credentials=True)
```

4.模块拆分之后,实例化app只有一次，如何注册蓝图和flask-restful

`Routes.py`

```python
# routes.py
from api import *
from flask import Blueprint
from flask_restful import Api

BlogApi = Blueprint('api', __name__, url_prefix='/v1')

docs = Api(BlogApi)
docs.add_resource(CreateLesson, '/admin/lession/', endpoint='lession')
```

`__init__.py`

```python
from routes import docs
blueprints = ['routes:BlogApi']

def createapp():
    docs.init_app(app)
    # 注册所有蓝图
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)
```

可以看出当不拆分模块的时候，应用注册都是 app.   现在使用`应用.init_app`去初始化app

5.顺便提一下logging的使用，不拆分模块时,log的使用

```python
try:
    ...
except Exception as e:
    app.logger.error(e)
```

但现在app实例化一次,在其他模块没法调用app，这时候可以使用`current_app`

```python
from flask import current_app

try:
    ...
except Exception as e:
    current_app.logger.error(e)
```



