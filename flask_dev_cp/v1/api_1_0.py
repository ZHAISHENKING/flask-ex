#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import flask
import bson.binary
import bson.objectid
import bson.errors
import json

from bson.objectid import ObjectId
from flask import Flask, redirect, make_response, current_app
from flask_restful import Resource
from .utilb import *
from .models import Student, Day, File


class Index(Resource):
    """
    主页
    """
    def get(self):
        html = """
            <!doctype html>
            <html>
            <body>
            <form action='upload/' method='post' enctype='multipart/form-data'>
             <input type="text" name="name">
             <input type="text" name="homeWork">
             <input type="textarea" name="comments">
             <input type="text" name="title">
             <input type="text" name="text">
             <input type='file' name='imgfile'>
             <input type='file' name='videofile'>
             <input type='text' name='kadaUrl'>
             <input type='submit' value='Upload'>
            </form>
        """
        return make_response(html)


class UploadAPI(Resource):

    def get(self):
        return redirect('https://course.ultrabear.com.cn/shareday')

    def post(self):
        data = request.values
        if request.files:
            image = request.files['imgfile']
            video = request.files['videofile']
            imageurl = save_file(image)
            videourl = save_file(video)
            if imageurl and videourl:
                print('---------------------------')
                print(data['name'])
                print(type(data['name']))
                print('---------------------------')
                student10 = {"name": data['name'],
                             "homeWork": data['homeWork'],
                             "comments": data['comments'],
                             "videofile": '/f/' + str(videourl),
                             "imgfile": '/f/' + str(imageurl),
                             "kadaUrl": data['kadaUrl'],
                             "title": data['title'],
                             "text": data['text'],
                             }

                student = Day(**student10).save()
                print(student['id'])
                print(type(student))
                student_id = student['id']
                student_ids = str(ObjectId(student_id))
                data = {
                    "code": 200,
                    "msg": "上传成功",
                    "data": student_ids
                }
                return responseto(data=data)
            return {'msg': '文件类型错误'}, 400
        return {'msg': '文件未上传'}, 400


class ServerFile(Resource):
    """
    查看作品视频
    """
    def get(self,id):
        md = File.objects(md5=id.split('.')[0])
        if md is None:
            raise bson.errors.InvalidId()
        resp = flask.Response(md['content'], mimetype=ALLOWED_EXTENSIONS[md['mime']])
        resp.headers['Last-Modified'] = md['time'].ctime()
        ctype = '*'
        if request.headers.get("Range"):
            range_value = request.headers["Range"]
            HTTP_RANGE_HEADER = re.compile(r'bytes=([0-9]+)\-(([0-9]+)?)')
            m = re.match(HTTP_RANGE_HEADER, range_value)
            if m:
                start_str = m.group(1)
                start = int(start_str)
                end_str = m.group(2)
                end = -1
                if len(end_str) > 0:
                    end = int(end_str)
                resp.status_code = 206
                resp.headers["Content-Type"] = ctype
                if end == -1:
                    resp.headers["Content-Length"] = str(md['size'] - start)
                else:
                    resp.headers["Content-Length"] = str(end - start + 1)
                resp.headers["Accept-Ranges"] = "bytes"
                if end < 0:
                    content_range_header_value = "bytes %d-%d/%d" % (start, md['size'] - 1, md['size'])
                else:
                    content_range_header_value = "bytes %d-%d/%d" % (start, end, md['size'])
                resp.headers["Content-Range"] = content_range_header_value
                resp.headers["Connection"] = "keep-alive"
        return resp


class HomeworkInfoAPI(Resource):
    """
    查看作品信息
    """
    def get(self, id):
        try:
            obj = Day.objects(_id=ObjectId(id))
            data = {
                "code": 200,
                "msg": "请求成功",
                "data": {
                    'name': obj["name"],
                    "homeWork": obj["homeWork"],
                    "comments": obj["comments"],
                    "videofile": obj["videofile"],
                    "imgfile": obj["imgfile"],
                    "title": obj["title"],
                    "text": obj["text"],
                    "kadaUrl": obj["kadaUrl"]
                }
            }
            return responseto(data=data)

        except Exception as e:
            return {'msg': '信息不存在'}, 404


class StudentAPI(Resource):
    """
    存储学生报名信息
    """
    def get(self):
        try:
            result = []
            obj = Student.objects.all()
            # obj = list(info_set.find())
            for i in obj:
                result.append({
                    "name": i['name'],
                    "phone": i["phone"],
                    "Fname": i['fname'],
                    "equipments": i["equipments"],
                    "grade": i["grade"],
                    "sex": i["sex"],
                    "city": i["city"]
                })
            data = {
                "code": 200,
                "msg": "请求成功",
                "data": result
            }
            return responseto(data=data)
        except Exception as e:
            current_app.logger.error(e)
            return {'code':400, 'msg': '信息不存在'}

    def post(self):
        data = request.get_json()
        print(data['name'])
        infoIO = {
            "name":data['name'],
            "phone":data["phone"],
            "fname":data['Fname'],
            "equipments":data["equipments"],
            "grade":data["grade"],
            "sex":data["sex"],
            "city":data["city"]
        }
        try:
            # user_id = info_set.insert_one(infoIO).inserted_id
            user = Student(**infoIO)
            user.save()
            # user_ids = str(ObjectId(user_id))
            data = {
                "code": 200,
                "msg": "上传成功",
                "data": {}
            }
            return responseto(data=data)
        except Exception as e:
            current_app.logger.error(e)
            return {"msg": "保存失败"}, 400


