# 请求成功
def trueReturn(data):
    return {
        "code": 0,
        "data": data,
        "msg": "请求成功"
    }


# 内部错误
def falseReturn(msg):
    return {
        "code": 1,
        "data": '',
        "msg": msg
    }


# 无权限
def VaildReturn(data):
    return {
        "code": 4,
        "data": data,
        "msg": "无效验证"
    }


# 数据库操作错误
def MongoReturn():
    return {
        "code": 2,
        "msg": "数据库操作错误"
    }


# JWT验证
def jwt_required(origin_func):
    def wrapper(self, *args, **kwargs):
        from flask import request
        from util.auth import Auth

        # 请求头是否包含"jwt"
        if "jwt" in request.headers:
            is_vaild, info = Auth.decode_auth_token(request.headers['jwt'])
            if is_vaild:
                fn = origin_func(self, *args, **kwargs)
                return fn
            else:
                return falseReturn(info)
        else:
            return VaildReturn("")
    return wrapper


# 错误判断
def catch_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        from flask import current_app
        from mongoengine.errors import (
            OperationError,
            FieldDoesNotExist,
            SaveConditionError,
            InvalidDocumentError,
            ValidationError,
            NotUniqueError,
            InvalidQueryError,
        )
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except AttributeError as e:
            return "参数错误"
        except (
            FieldDoesNotExist,
            SaveConditionError,
            InvalidQueryError,
            InvalidDocumentError,
            ValidationError,
            NotUniqueError,
            OperationError
        ) as e:
            current_app.logger.error(e)
            return MongoReturn()
        except TypeError as e:
            current_app.logger.error(e)
            return falseReturn("TypeError")
        except Exception as e:
            current_app.logger.error(e)
            return falseReturn("Error")

    return wrapper
