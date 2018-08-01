#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app import db
import datetime


class Tags(db.Document):
    name = db.StringField(max_length=50)
    get_count = db.IntField(default=0)
    create_time = db.DateTimeField(
        default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def tags_number():
        return Tags.objects.count()

    def to_dict(self):
        result = dict()

        result['name'] = self.name
        result['get_count'] = self.get_count
        result['create_time'] = self.create_time.strftime("%Y-%m-%d %H:%M:%S")

        return result

    def __repr__(self):
        return "<Tags - %s>" % self.name


class Message(db.EmbeddedDocument):
    post = db.StringField()
    post_id = db.StringField()
    who = db.StringField()
    time = db.DateTimeField(default=datetime.datetime.now())

    meta = {
        'ordering': ['-time']
    }

    def to_dict(self):
        result = dict()

        result['post'] = self.post
        result['post_id'] = self.post_id
        result['who'] = self.who
        result['time'] = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return result

    def __repr__(self):
        return "<Message %s>" % self.post
