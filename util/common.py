import requests, json, time
import hashlib
from dateutil.parser import parse
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from datetime import *


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
            current_app.logger.error(e)
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


def time_temp(tmp):
    """
    时间表模版序列化
    :param tmp:
    :return templateObj:
    """
    b, *W = tmp.split(';')
    Y, M, *c = b.split("/")
    templateObj = []
    for i in W:
        w, h = i.split("/")
        templateObj.append({
            "year": Y,
            "month": M,
            "week": w,
            "times": h
        })
    return templateObj


def time_stu(tmp):
    """
    学生时间序列化
    return studentObj
    """
    t, *h = tmp.split(" ")
    tim = parse(tmp)
    studentObj = {
        "year": tim.year,
        "month": tim.month,
        "week": str(tim.weekday()+1),
        "times": h[0]
    }
    return studentObj


# 对比时间段
def Timeslots(temp, stu):
    if temp["times"] == "*" or temp["times"] == stu["times"]:
        return True
    else:
        return False


# 对比周
def Weel(temp, stu):
    if temp["week"] == "*" or temp["week"] == stu["week"]:
        return Timeslots(temp, stu)
    else:
        return False


# 对比月份
def Month(temp, stu):
    if temp["month"] == "*" or temp["month"] == stu["month"]:
        return Weel(temp, stu)
    else:
        return False


# 模板时间merge
def MatchTime(temp, stu):
    if temp["year"] == "*" or temp["year"] == stu["year"]:
        return Month(temp, stu)
    else:
        return False


class ClassIn(object):
    """
    classin相关接口
    """
    def __init__(self):
        from flask import current_app

        self.sid = current_app.config["SID"]
        t = str(int(time.time()))
        self.key = md(current_app.config["SECRET_KEY"] + t)
        self.hearders = {
            "Host": "www.eeo.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }

    # 创建教室获取classIn教室id
    def get_class_in_id(self, course):
        url = "http://www.eeo.cn/partner/api/course.api.php?action=addCourse"
        data = {
            "SID": self.sid,
            "safeKey": self.key,
            "timeStamp": int(time.time()),
            "courseName": course

        }
        r = requests.post(url, data=data, headers=self.hearders)
        return r.json()

    # 创建课节
    def create_lesson(self, id, *c):
        url = "http://www.eeo.cn/partner/api/course.api.php?action=addCourseClassMultiple"
        data = {
            "SID": self.sid,
            "safeKey": self.key,
            "timeStamp": int(time.time()),
            "courseId": id,
            "classJson": c
        }
        r = requests.post(url, data=data, headers=self.hearders)
        return r.json()


# md5散列值
def md(t):
    hash1 = hashlib.md5()
    hash1.update(t.encode("UTF-8"))
    to_hash = hash1.hexdigest()
    return to_hash


def lesson_time(temp, start, num):
    """
    :param temp: 2018/09/;2/9:00;3/13:00;5/13:00
    :param start:2018/08/22 16:26
    :param num: 20
    :return:
    """
    config_choice = {
        "1": MO,
        "2": TU,
        "3": WE,
        "4": TH,
        "5": FR,
        "6": SA,
        "7": SU
    }

    temp = time_temp(temp)
    slag = temp[0]
    stu = time_stu(start)
    # 学生时间段与模版匹配 year
    if slag["year"] == "*" or stu["year"] <= slag["year"]:
        # 匹配 month
        if slag["month"] == "*" or stu["month"] <= slag["month"]:
            week_list = [i["week"] for i in temp]

            # 使用dateutil.rrule库获取开始num节上课日期
            r = rruleset()
            r.rrule(rrule(
                WEEKLY,
                dtstart=parse(start),
                count=num,
                byweekday=[config_choice[i] for i in week_list]
            ))
            datetime_list = list(r)

            # 修改上课具体时间
            for i in temp:
                for index, j in enumerate(datetime_list):
                    if int(i["week"]) == j.weekday()+1:
                        h, m = i["times"].split(":")
                        datetime_list[index] = datetime(j.year, j.month, j.day, int(h), int(m))

            c = TimeFomat()
            result = [c.ms(i) for i in datetime_list]
            return result
    else:
        return


class TimeFomat(object):
    """时间处理类"""

    def ms(self, d):
        import time
        # 给定时间元组,转换为毫秒
        return int(time.mktime(d.timetuple()))
