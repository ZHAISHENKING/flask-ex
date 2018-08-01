#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import random
import string
from threading import Thread

from flask import url_for
from flask_mail import Message

from app import mail
from manage import app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def get_random_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


def send_mail(email):
    msg = Message('来自Fly Blog找回密码的邮件', recipients=[email])
    msg.body = '您要找回你的密码啦'
    code = get_random_code()
    url = url_for('user.change_pw', code=code, _external=True)
    msg.html = '<b>下次可要记住你的密码哟!"</b><br>' + "<a href=" + url + "/>" + url + "<br><br><b>点上面的链接,亲</b>"

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return code
