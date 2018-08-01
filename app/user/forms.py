#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField , StringField, PasswordField
# from flask_wtf.file import FileRequired ,FileField


class RegForm(FlaskForm):

    email = StringField(
        render_kw={
            "class":"form-control",
            "placeholder":"邮箱"
        }
    )

    text = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "昵称"
        }
    )

    password1 = PasswordField(
        render_kw={
            "class": "form-control",
            "placeholder": "密码"
        }
    )

    password2 = PasswordField(
        render_kw={
            "class": "form-control",
            "placeholder": "再输入一次密码"
        }
    )

    directions = StringField(
        render_kw={
            "class":"form-control",
            "placeholder":"个性签名"
        }
    )

    get_tags = StringField(
        render_kw={
            "class":"form-control",
            "placeholder":"兴趣"
        }
    )

    submit = SubmitField(
        _name="注册",
        render_kw={
            "class":"btn btn-primary",
            "style":"width: 250px;height: 39px;"
        }
    )
    # imgs_upload = FileField(
    #     _name="头像上穿",
    #     validators=[FileRequired()],
    #     render_kw={
    #         # "class": "form-control"
    #     }
    # )


class LoginForm(FlaskForm):
    text = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "昵称"
        }
    )
    password = PasswordField(
        render_kw={
            "class": "form-control",
            "placeholder": "密码"
        }
    )
    submit = SubmitField(
        _name="注册",
        render_kw={
            "class": "btn btn-primary",
            "style": "width: 250px;height: 39px;"
        }
    )

class InputEmailForm(FlaskForm):
    email = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "邮箱"
        }
    )
    submit = SubmitField(
        _name="发送",
        render_kw={
            "class": "btn btn-primary",
            "style": "width: 250px;height: 39px;"
        }
    )

class ChangePwForm(FlaskForm):
    code = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "验证码"
        }
    )
    password1 = PasswordField(
        render_kw={
            "class": "form-control",
            "placeholder": "密码"
        }
    )

    password2 = PasswordField(
        render_kw={
            "class": "form-control",
            "placeholder": "再输入一次密码"
        }
    )
    submit = SubmitField(
        _name="完成",
        render_kw={
            "class": "btn btn-primary",
            "style": "width: 250px;height: 39px;"
        }
    )
