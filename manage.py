#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_script import Manager

from app import create_app
from app.admin.models import Admin
from app.public.models import Tags

app = create_app('production')

manager = Manager(app)


@manager.command
def create_admin():
    name = 'admin'
    password = 'maxin123'
    admin = Admin(name=name)
    admin.password = password
    admin.save()
    print("ok, you successful create a admin")


@manager.command
def create_tags():
    tags_list = ['编程', 'Python', 'java', '计算机',
                 '动漫', '人工智能', 'C++', '美女', '帅哥', '人生']
    for tag_name in tags_list:
        tag = Tags(name=tag_name)
        tag.save()
    print("ok, you successful create many tags")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)
