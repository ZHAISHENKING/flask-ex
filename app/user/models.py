# /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from flask import current_app
from flask_login import UserMixin
from mongoengine.queryset.visitor import Q
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app.public.models import Tags, Message
from app.public.middleware import get_tags
from app import db, login_manager


class User(UserMixin, db.Document):
    email = db.EmailField(max_length=255)
    name = db.StringField(max_length=50)
    password_hash = db.StringField(max_length=155)
    avatar_img_url = db.StringField(
        max_length=100, default="avatar.jpg")  # 头像路径
    messages = db.ListField(db.EmbeddedDocumentField(Message))
    view_messages = db.ListField(db.EmbeddedDocumentField(Message))
    get_tags = db.ListField(db.ReferenceField(
        Tags, reverse_delete_rule=1), dbref=True, check_reference=False)  # 兴趣集
    create_time = db.DateTimeField(
        default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    directions = db.StringField()  # 个性签名
    post_number = db.IntField(default=0)  # 文章数量
    comments_number = db.IntField(default=0)  # 评论数量

    meta = {
        'indexes': ['name']}

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.name}).decode('utf-8')

    def messages_number(self):
        return len(self.messages)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_views_message(self, post_id, post_title):
        """add user'mesages when user view some posts"""
        mes = Message(post_id=post_id, post=post_title)
        self.update(push__view_messages=mes)

    def get_id(self):
        try:
            return self.name
        except AttributeError:
            raise NotImplementedError(
                'No `username` attribute - override `get_id`')

    def to_dict(self):
        result = dict()

        result['name'] = self.name
        result['email'] = self.email
        result['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        result['directions'] = self.directions
        result['get_tags'] = [tag.to_dict() for tag in self.get_tags]
        result['post_number'] = self.post_number

        return result

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User - %s>' % self.name

    @staticmethod
    def create(name, email, directions, password, get_tag):
        """create new user"""
        user = User(name=name, email=email, directions=directions)
        user.password = password
        user.get_tags = get_tags(get_tag)
        user.save()

    @staticmethod
    def users_number():
        return User.objects.count()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.objects.get(name=data['name'])

    @staticmethod
    def find_user(input_text):
        """find user by username or email to login user"""
        user = User.objects(Q(name=input_text) | Q(email=input_text)).first()
        if user is None:
            return False
        return user

    
@login_manager.user_loader
def load_user(user_name):
    try:
        user = User.objects.get(name=user_name)
        if user:
            return user
    except User.DoesNotExist:
        return None
