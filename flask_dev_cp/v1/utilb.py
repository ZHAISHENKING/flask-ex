#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,re, hashlib, time, datetime, pymongo
from bson import binary, objectid, errors
from .config import ALLOWED_EXTENSIONS
from io import BytesIO
from flask import jsonify, request
from werkzeug.utils import secure_filename
from .models import File


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_file(f):
    content = BytesIO(f.read())
    content.seek(0, os.SEEK_END)
    size = content.tell()
    content.seek(0, os.SEEK_SET)
    try:
        filename = secure_filename(f.filename)
        if filename:
            if '.' in filename:
                mime = filename.rsplit('.', 1)[1]
            else:
                mime = filename
        t = str(time.time())
        str1 = filename + t
        hash1 = hashlib.md5()
        hash1.update(str1.encode('UTF-8'))
        toHash = hash1.hexdigest()
        id = toHash + "." + mime
        if mime not in ALLOWED_EXTENSIONS.keys():
            raise IOError()
    except IOError:
        return 0
    c = dict(
        content=binary.Binary(content.getvalue()),
        mime=mime,
        time=datetime.datetime.utcnow(),
        md5=toHash,
        filename=filename,
        size=size
    )
    try:
        file = File(**c)
        file.save()
    except pymongo.errors.DuplicateKeyError:
        return jsonify({
            "code": 400,
            "msg": "数据保存失败",
        })
    return id


def responseto(message=None, error=None, data=None, **kwargs):
    if not data:
        data = kwargs
        data['error'] = error
        if message:
            data['message'] = message
            if error is None:
                data['error'] = True
        else:
            if error is None:
                data['error'] = False
    if not isinstance(data, dict):
        data = {'error':True, 'message':'data 必须是一个 dict！'}
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    return resp
