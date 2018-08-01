# /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime


from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Admin(db.Document):
    """后台管理员模型"""

    name = db.StringField(max_length=60)
    password_hash = db.StringField(max_length=155)
    last_time = db.DateTimeField(default=datetime.datetime.now(
    ).strftime("%Y-%m-%d %H:%M:%S"), required=True)
    login_number = db.IntField(default=0)

    def get_id(self):
        try:
            return self.name
        except AttributeError:
            raise NotImplementedError(
                'No `username` attribute - override `get_id`')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __unicode__(self):
        return self.name
