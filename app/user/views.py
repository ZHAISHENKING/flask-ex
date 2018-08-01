#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os

from flask import request, jsonify, redirect, url_for, render_template, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename


from . import user
from .email import send_mail
from .forms import RegForm, LoginForm, InputEmailForm, ChangePwForm
from .models import User
from ..main.models import Post


@user.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get("email")
    if User.objects(email=email):
        return jsonify(False)
    return jsonify(True)

@user.route('/user_one/<string:name>')
def user_one(name):
    user = User.objects(name=name).first()
    return jsonify(user.to_dict())


@user.route('/check-username', methods=['POST'])
def check_username():
    name = request.form.get("text")
    if User.objects(name=name):
        return jsonify(False)
    return jsonify(True)


@user.route('/register', methods=['POST', 'GET'])
def register():
    """user register"""
    form = RegForm()
    if form.validate_on_submit():
        form_data = form.data
        password1 = form_data['password1']
        email = form_data['email']
        name = form_data['text']
        directions = form_data['directions']
        get_tag = form_data['get_tags'].split()
        User.create(name, email, directions, password1, get_tag)
        return redirect(url_for('user.login'))
    return render_template("main/register.html", form=form)


@user.route('/login', methods=['POST', 'GET'])
def login():
    """user login"""
    form = LoginForm()
    if form.validate_on_submit():
        input_text = form.text.data
        password = form.password.data
        user = User.find_user(input_text)
        if user:
            is_right = user.verify_password(password)
            if is_right:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash("密码错误!")
        else:
            flash("用户名错误或邮箱错误!")
    return render_template('main/login.html', form=form)


@user.route('/logout')
def logout():
    """user logout"""
    logout_user()
    return redirect(url_for('main.index'))


@user.route('/find_password', methods=['POST', 'GET'])
def find_password():
    """find back user's password"""
    form = InputEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.objects(email=email).first()
        session['code'] = send_mail(email)
        session['change_user'] = user.name
        if session['code']:
            flash("发送成功了, 请到邮箱中查看")
        else:
            flash("邮箱发送失败")
    return render_template('user/input_email.html', form=form)


@user.route('/change_pw/<string:code>', methods=['GET', 'POST'])
def change_pw(code):
    form = ChangePwForm()
    if form.validate_on_submit():
        if session['code'] == code:
            password_hash = form.password1.data
            user = User.objects.get(name=session['change_user'])
            user.password = password_hash
            user.save()
            return redirect(url_for('user.login'))
    return render_template('user/change_pw.html', form=form)


@user.route('/index')
@login_required
def index():
    return render_template('user/user_index_base.html')


@user.route('/user_articles')
def user_articles():
    user = User.objects(name=current_user.name).first()
    page = request.args.get('page', 1, type=int)
    content = {
        "user_articles": Post.objects(author=user).paginate(page=page, per_page=8, error_out=False)
    }
    return render_template('user/user_article.html', **content)


@user.route('/user_messages')
def user_messages():
    user = User.objects(name=current_user.name).first()
    page = request.args.get('page', 1, type=int)
    content = {
        "user_messages": user.messages
    }
    return render_template('user/user_messages.html', **content)


@user.route('/user_views_messages')
def user_views_messages():
    user = User.objects(name=current_user.name).first()
    page = request.args.get('page', 1, type=int)
    content = {
        "user_views_messages": user.view_messages
    }
    return render_template('user/user_views_messages.html', **content)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@user.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ex = os.path.splitext(filename)[1]
            filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ex
            current_user.update(avatar_img_url=filename)
            file.save(os.path.join(current_app.config['SAVEPIC'], filename))
            return redirect(url_for('user.index'))


@user.errorhandler(400)
def page_not_found(e):
    return render_template('error.html'), 400
