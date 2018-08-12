from v1.api_1_0 import *
from flask import Blueprint
from flask_restful import Api

# 注册蓝图,路由前缀为/docs
uploadApi = Blueprint('api', __name__, url_prefix='/docs')

docs = Api(uploadApi)

docs.add_resource(Index,'/', endpoint='home')                                   # 测试表单
docs.add_resource(ServerFile, '/f/<id>/', endpoint='serverfile')                # 文件展示
docs.add_resource(UploadAPI, '/upload/', endpoint='upload')                     # 上传接口
docs.add_resource(HomeworkInfoAPI, '/student_all/<id>/', endpoint='homeinfo')   # 获取作品信息
docs.add_resource(StudentAPI,'/student/', endpoint='student')                 # 添加学生报名信息

