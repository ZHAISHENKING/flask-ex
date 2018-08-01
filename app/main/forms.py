#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField , StringField, PasswordField , SelectField
from wtforms.validators import DataRequired



class CommentsForm(FlaskForm):
    comments_text = TextAreaField(

        render_kw={
            "style" : "margin-left: 5px;height: 96px",
            "placeholder": "请输入内容"
        }
    )

    submit = SubmitField(
        "提交",
        render_kw={
            "class":"btn btn-send"
        }
    )



class AddPostForm(FlaskForm):

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
    get_tags = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "兴趣"
        }
    )
    submit = SubmitField(
        '发布',
        id='signinSubmit',
        render_kw={
            "class": "btn btn-lg btn-primary btn-block"
        })

