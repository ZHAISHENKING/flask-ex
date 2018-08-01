# /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os



from flask import render_template, redirect, url_for, request, jsonify, Response, session

from app.main.models import Post, Tags
from app.user.models import User
from app.public.middleware import admin_login_required, get_host_ip
from config import Config
from . import admin
from .forms import AdminForm, AddArticleForm
from .models import Admin





@admin.route('/login', methods=['POST', 'GET'])
def login():
    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        user = Admin.objects.get(name=username)
        if user and user.verify_password(form.password.data):
            user.last_time = datetime.datetime.now
            user.login_number += 1
            user.save()
            session['user_name'] = username
            return redirect(url_for('admin.index'))
        return "密码错误！"
    return render_template('admin/login.html', form=form)


@admin.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {'success': 0, 'message': '图片格式错误'}
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(Config.SAVEPIC, filename).replace('\\', '/'))
        res = {'success': 1, 'message': "图片上传成功", 'url': url_for('admin.image', name=filename)}
    return jsonify(res)


@admin.route('/image/<name>', methods=['GET'])
def image(name):
    with open(os.path.join(Config.SAVEPIC, name), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp


@admin.route('/logout')
def logout():
    session.pop("user_name", None)
    return redirect(url_for('admin.login'))


@admin.route('/index')
@admin_login_required
def index():
    content = {'ip': get_host_ip(), 'post_number': Post.objects.count(),
               'login_time': Admin.objects.first().last_time,
               'login_number': Admin.objects.first().login_number, }
    return render_template('admin/index.html', **content)


@admin.route('/article')
@admin_login_required
def article():
    page = request.args.get('page', 1, type=int)
    content = {'articles': Post.objects.paginate(page=page, per_page=8, error_out=False)}
    return render_template('admin/article.html', **content)


@admin.route('/add-article', methods=['POST', 'GET'])
@admin_login_required
def add_article():
    form = AddArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        tag_name = form.keywords.data
        tag = Tags.objects(name=tag_name).first()
        post = Post(title=title, body=body)
        post.tags.append(tag)
        post.save()
        return redirect(url_for('admin.article'))
    return render_template('admin/add-article.html', form=form)


@admin.route('/delete_post/<post_id>/')
@admin_login_required
def delete_post(post_id):
    post = Post.objects.get_or_404(id=post_id)
    post.delete()
    return redirect(url_for('admin.article'))


@admin.route('/tags')
@admin_login_required
def tags():
    page = request.args.get('page', 1, type=int)
    content = {'tags': Tags.objects.paginate(page=page, per_page=8, error_out=False)}
    return render_template('admin/tags.html', **content)


@admin.route('/delete_tag/<tag_id>/')
@admin_login_required
def delete_tag(tag_id):
    tag = Tags.objects.get_or_404(id=tag_id)
    tag.delete()
    return redirect(url_for('admin.tags'))


@admin.route('/users')
@admin_login_required
def users():
    page = request.args.get('page', 1, type=int)
    content = {'users': User.objects.paginate(page=page, per_page=8, error_out=False)}
    return render_template('admin/users.html', **content)


@admin.route('/delete_user/<user_id>/')
@admin_login_required
def delete_user(user_id):
    user = User.objects.get_or_404(id=user_id)
    user.delete()
    return redirect(url_for('admin.users'))
