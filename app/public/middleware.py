#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
from functools import wraps

from flask import redirect, session, url_for

from .models import Tags


def get_tags(tags_list):
    tags_result = []
    for tag_name in tags_list:
        tag = Tags.objects(name__icontains=tag_name).first()
        if tag is None:
            tag = Tags()
            tag.name = tag_name
            tag.save()
        tag.update(inc__get_count=1)
        tags_result.append(tag)
    return tags_result


def admin_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_name'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))

    return wrapper


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
