# /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from app import db
from flask import url_for
from mongoengine.queryset.visitor import Q
from flask_login import current_user
from app.user.models import User
from app.public.models import Tags, Message
from app.public.middleware import get_tags


class Comments(db.EmbeddedDocument):
    text = db.StringField()
    author = db.ReferenceField(User)
    create_time = db.DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "<Comment %s>" % self.text[:6]


class Post(db.Document):
    title = db.StringField(max_length=120, default='new blog')
    body = db.StringField(required=True)
    author = db.ReferenceField(User, reverse_delete_rule=2)
    tags = db.ListField(db.ReferenceField(
        Tags, reverse_delete_rule=1))  # 嵌入文档列表
    comments = db.ListField(db.EmbeddedDocumentField(Comments))
    img_url = db.StringField(default="post_img.jpg")
    create_time = db.DateTimeField(default=datetime.datetime.now())
    post_views = db.IntField(default=0)
    post_likes = db.IntField(default=0)
    comments_number = db.IntField(default=0)

    meta = {
        'ordering': ['-create_time'],
        'indexes': ['post_views', 'title']}


    def to_dict(self):
        result = dict()

        result['title'] = self.title
        result['post_url'] = url_for(
            'api_v1.post_view', post_id=self.id, _external=True)
        result['author'] = self.author.name
        result['body'] = self.body
        result['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        result['tags'] = [tag.to_dict() for tag in self.tags]
        result['post_views'] = self.post_views
        result['comments_number'] = self.comments_number

        return result

    @staticmethod
    def search_text(keyword):
        """search text by input"""
        result = Post.objects(Q(title__icontains=keyword)
                              | Q(body__icontains=keyword))
        return result

    @staticmethod
    def create(title, body, author, img_url, tags):
        post = Post(title=title, body=body, author=author, img_url=img_url)
        post.tags = get_tags(tags)
        post.save()
        return True

    @staticmethod
    def add_messages_user(post_id):
        """add user comment info to post of author's messages"""
        post = Post.objects.get(id=post_id)
        message = Message(post=post.title, post_id=post_id,
                          who=current_user.name)
        post.author.update(push__messages=message)

    @staticmethod
    def post_number():
        return Post.objects.count()

    @staticmethod
    def find_tags(tag_list):
        """ :return tags by user like"""
        tag_list_len = len(tag_list)
        if tag_list_len == 0:
            return Post.objects.all()
        if tag_list_len == 1:
            return Post.objects(tags__in=[tag_list[0]])
        if tag_list_len == 2:
            return Post.objects(Q(tags__in=[tag_list[0]])
                                | Q(tags__in=[tag_list[1]]))
        else:
            return Post.objects(Q(tags__in=[tag_list[1]])
                                | Q(tags__in=[tag_list[1]])
                                | Q(tags__in=[tag_list[2]]))

    def __repr__(self):
        return '<Post - %s>' % self.title
