#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from app.main.models import Tags


def tags_choices():
    tags = Tags.objects.all()
    choices_list = []
    if tags is not None:
        for i in tags:
            choices = (i.name,i.name)
            choices_list.append(choices)
        return choices_list
    else:
        return None

class AdminForm(FlaskForm):
    username =  StringField(
        validators=[
            DataRequired('请输入账号')
        ],
        id="userName",
        description="账号",
        render_kw={
            "class":"form-control",
            "placeholder":"请输入用户名"
        }

    )

    password = PasswordField(
        validators=[
            DataRequired('请输入密码')

        ],
        id="userPwd",
        description="密码",
        render_kw={
            "class":"form-control",
            "placeholder": "请输入密码"
        }
    )

    submit = SubmitField(
        '登录',
        id = 'signinSubmit',
        render_kw={
            "class": "btn btn-lg btn-primary btn-block"
        }
    )

class AddArticleForm(FlaskForm):

    title = StringField(
        validators=[
            DataRequired("请输入标题")
        ],
        id="article-title",
        render_kw={
            "class": "form-control",
            "autocomplete" : "off",
            "placeholder" : "在此处输入标题"
        }
    )
    body = TextAreaField(
        id="ts",
        render_kw={
            "class":"form-control",
            "style" : "display:none"
        }
    )
    keywords = SelectField(
    'Programming Language',
        choices=tags_choices(),
        render_kw={
            "class":"form-control",
            "placeholder":"请输入关键字",
            "autocomplete":"off"
        }
    )
    submit = SubmitField(
        '发布',
        id='signinSubmit',
        render_kw={
            "class": "btn btn-lg btn-primary btn-block"
        })