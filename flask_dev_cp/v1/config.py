import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import current_app

MONGODB_SETTINGS = {
        'DB': 'ultrabear_homework',
        'USERNAME': None,
        'PASSWORD': None,
        'HOST': 'localhost',
        'PORT': 27017
    }

# 可上传的文件类型
ALLOWED_EXTENSIONS=dict([
            ("3gp",    "video/3gpp"),
            ("gif",    "image/gif"),
            ("jpeg",   "image/jpeg"),
            ("jpg",    "image/jpeg"),
            ("m4u",    "video/vndmpegurl"),
            ("m4v",    "video/x-m4v"),
            ("mov",    "video/quicktime"),
            ("mp4",    "video/mp4"),
            ("mpe",    "video/mpeg"),
            ("mpeg",   "video/mpeg"),
            ("mpg",    "video/mpeg"),
            ("mpg4",   "video/mp4"),
            ("png",    "image/png"),
            ("flv", "flv-application/octet-stream")
        ])


# # 连接mongo
# def MongoConn():
#     try:
#         CLIENT = MongoClient('localhost:27017', serverSelectionTimeoutMS=3).ultrabear_homework
#         # CLIENT = MongoClient('mongodb://jamie:jamie199469@localhost:27676/ultrabear_homework', serverSelectionTimeoutMS=3).ultrabear_homework
#         return CLIENT
#     except ConnectionFailure as e:
#         current_app.logger.error(e)
#         return
