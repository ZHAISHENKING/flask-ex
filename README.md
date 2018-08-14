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



### 未解决问题

------

由于mongo本身使用就少，mongoengine使用文档百度不超过一页,所有很多问题需要谷歌，查看英文文档，现在仍有些问题未解决

1.使用mongoengine如何迁移数据库,   因为mongoengine这个第三方库一直在维护，使用群体多，而且比起其他mongo orm成熟些，所以使用的mongoengine

2.pyjwt在与其他后台语言对接时如何使用，为了防止api被爬取，使用jwt进行验证, go语言写的user，为在用python时怎么去添加jwt校验


# Mongoengine



### 连接

`connect`

```bash
connect（db = None，alias ='default'，** kwargs ）
```

### 多数据库支持

`register_connection`

```bash
register_connection(
	alias="default",
    db=None,
    name=None,
    host=None,
    port=None,
    username=None,
    password=None
    )
```

`models`中切换

```python
from MongoEngine import *

class User(Document):
    name = StringField()
    meta = {
        "db_alias": "default"
    }
```

### 字段

`StringField`	字符串

`URLField`		Url

`EmailField`		邮箱地址字段

`Intfield`		32位整数

`LongField`		64位整数

`FloatField`		浮点数字段

`DecimalField`	定点十进制

`BooleanField`	布尔

`DateTimeField`	时间

`ComplexDateTimeField`	精确毫秒级时间

`EmbeddedDocumentField`	嵌入式文档，有声明的document_type

`GenericEmbeddedDocumentField`	通用嵌入式文档

`DynamicField`	动态字段类型

`ListField`		列表字段

`EmbeddedDocumentListField`	嵌入式有文件的List字段

`SortedListField`	排序的列表字段，确保始终检索为已排序的列表

`DictField`			字典

`MapField`			名称映射到指定字段

`ReferenceField`		文档引用

```bash
# 使用reverse_delete_rule可以处理删除字段引用的文档时应该发生的情况。
DO_NOTHING（0） - 不做任何事情（默认）。
NULLIFY（1） - 更新对null的引用。
CASCADE（2） - 删除与参考相关的文档。
拒绝（3） - 防止删除参考对象。
PULL（4） - 从ListField参考文献中拉出参考

初始化参考字段。

参数：	
dbref - 将引用存储DBRef 为ObjectId.id 或.id。
reverse_delete_rule - 确定删除引用对象时要执行的操作
```



`LazyReferenceField`

`GenericReferenceField`

`BinaryField`		二进制数据字段

`FileField`			GirdFS存储字段

`ImageField`			图像文件存储字段

`SequenceField`

`ObjectIdField`

`UUIDField`

`GridFSProxy`

`ImageGridFsProxy`

`ImproperlyConfigured`



### 查询

> all()

​	返回所有文档

> all_fields()

​	包括所有字段

```python
post = BlogPost.objects.exclude('comments').all_fields()
```

> as_pymongo()

​	返回的不是Document实例 而是pymongo值

> batch_size()

`	限制单个批处理中返回的文档书

> clone()

​	创建副本

> comment(text)

​	查询中添加注释

> count(with_limit_and_skip=False)

​	数量

> create(**kwargs)

​	创建新对象，返回保存的对象实例

> delete（*write_concern = None*，*_from_doc_delete = False*，*cascade_refs = None* ）

​	删除查询匹配 的文档

| 参数： | **write_concern** - 向下传递额外的关键字参数，这些参数将用作结果`getLastError`命令的选项 。例如， 将等到至少两个服务器已记录写入并将强制主服务器上的fsync。`save(..., write_concern={w: 2, fsync: True}, ...)`**_from_doc_delete** - 从文档删除调用时为True，因此信号将被触发，因此不要循环。 |
| ------ | ------------------------------------------------------------ |
|        | 返回已删除的文档数量                                         |

> exec_js(*code*, *fields, **options)

​	执行js代码

| 参数： | **code** - 要执行的一串Javascript代码**fields** - 您将在函数中使用的字段，它们将作为参数传递给您的函数**选项** - 您希望函数可用的选项（通过`options`对象在Javascript中访问） |
| ------ | ------------------------------------------------------------ |
|        |                                                              |

> fields（*_only_called = False*，**\* kwargs* ）

​	处理如何加载此文档的字段

仅包含字段的子集：

```python
posts = BlogPost.objects().fields（author = 1，title = 1）
```

排除特定字段：

```python
posts = BlogPost.objects().fields（comments = 0）
```

要检索数组元素的子范围：

```python
posts = BlogPost.objects().fields（slice__comments = 5）
```

> filter()

​	过滤, 别名`__call__()`

> first()

​	匹配的第一个对象

> from_json(json_data)

​	将json数据转换为未保存的对象

> hint(index=None)

​	提示， 在对多个字段进行查询时，将索引字段作为提示传递，若索引不存在，提示不会执行任何操作

​	可以极大提高查询性能

> in_bulk(object_ids)

​	通过其id检索一组文档

| 参数：     | **object_ids** - `ObjectId`s 的列表或元组             |
| ---------- | ----------------------------------------------------- |
| 返回类型： | ObjectIds的dict作为键，集合特定的Document子类作为值。 |

> insert()

​	批量插入文档

> item_frequencies（*field*，*normalize = False*，*map_reduce = True* ）

​	返回整个查询文档集中字段中存在的所有项的字典及其对应的频率。这对于生成标记云或搜索文档很有用。

> limit(n)

​	返回的文档数限制为n，也可以用切片,如`User.objects[:5]`

> max_time_ms(ms)

​	服务器上终止查询前等待ms毫秒

> modify(*upsert = False*，*full_response = False*，*remove = False*，*new = False*，**\* update* )

​	更新并返回更新的文档。

​	基于新 参数返回修改之前或之后的文档。如果没有文档与查询匹配且upsert为false，则返回`None`。如果		upserting和new为false，则返回`None`。

​	如果full_response参数是`True`，则返回值将是来自服务器的整个响应对象，包括'ok'和'lastErrorObject'字段，而不仅仅是修改后的文档。这很有用，主要是因为'lastErrorObject'文档包含有关命令执行的信息。

| 参数： | **upsert** - 如果文档不存在则插入（默认`False`）**full_response** - 从服务器返回整个响应对象（默认情况下`False`，不适用于PyMongo 3+）**删除** - 删除而不是更新（默认`False`）**new** - 返回更新而不是原始文档（默认`False`）**更新** - Django样式的更新关键字参数 |
| ------ | ------------------------------------------------------------ |
|        |                                                              |

> next()

​	将结果包装在document对象中

> no_cache()

​	转换非缓存查询集

> no_dereference()

​	解除对此查询集的结果引用

> no_sub_classes()

​	仅返回此文档实例，不返回继承文档

> only()

​	仅加载此文档的子集

only（）是可链接的并且将执行union ::所以使用以下内容它将同时获取：title和author.name：

```
post = BlogPost.objects.only('title').only('author.name')
```

> order_by(*keys)

​	结果通过key来指定顺序，升降序

> scalar(*field)

​	不返回document实例，按顺序返回特定值或元组值

​	可以与`no_dereference()`关闭解除一起使用

> search_text(text,language=None)

​	使用文本索引开始文本搜索

> skip(n)

​	返回结果前跳过n个文档

> timeout(enabled)

​	查询时启用或禁用默认的超时

> to_json()

​	将查询集转换为json

> update(*upsert = False*，*multi = True*，*write_concern = None*，*full_result = False*，**\* update* )

​	更新

| 参数： | **upsert** - 如果文档不存在则插入（默认`False`）**multi** - 更新多个文档。**write_concern** - 向下传递额外的关键字参数，这些参数将用作结果`getLastError`命令的选项 。例如， 将等到至少两个服务器已记录写入并将强制主服务器上的fsync。`save(..., write_concern={w: 2, fsync: True}, ...)`**full_result** - 返回完整的结果字典，而不仅仅是更新的数字，例如return。`{'n': 2, 'nModified': 2, 'ok': 1.0, 'updatedExisting': True}`**更新** - Django样式的更新关键字参数 |
| ------ | ------------------------------------------------------------ |
|        |                                                              |

