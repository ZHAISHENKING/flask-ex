#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, current_app
from pyecharts import Bar

from app.public.middleware import admin_login_required
from . import data
from .database import TagsApi, UserApi


def tags_show():
    bar = Bar()
    data_api = TagsApi()
    tags_name, tags_counts = data_api.get_tags
    bar.add("FlyBlog 文章分类图", tags_name, tags_counts,
            xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30)
    return bar


def user_show():
    bar = Bar()
    data_api = UserApi()
    user_name, user_count = data_api.get_user
    bar.add("FlyBlog 用户资源图", user_name, user_count,
            xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30)
    return bar


@data.route('/data_show')
@admin_login_required
def index():
    tag_bar = tags_show()
    user_bar = user_show()
    content = {

        "myechart_user": user_bar.render_embed(),
        "myechart_tags": tag_bar.render_embed(),
        # "host":  current_app.config['REMOTE_HOST'],
        # "script_tags" : tag_bar.get_js_dependencies(),
        # "script_users": user_bar.get_js_dependencies()
    }
    return render_template("data/render.html", **content)
