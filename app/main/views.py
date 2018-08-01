# /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os

from flask import render_template, redirect, url_for, request, jsonify, Response, session
from flask_login import login_required, current_user

from app import cache
from app.user.models import User
from config import Config
from . import main
from .forms import AddPostForm
from .models import Post, Comments


@main.route('/', methods=['GET'])
def index():
    """ index """
    if current_user.is_authenticated:
        post_by_tags = Post.find_tags(current_user.get_tags)
    else:
        post_by_tags = None
    page = request.args.get('page', 1, type=int)
    content = {
        'top_articles': post_by_tags,
        'articles': Post.objects.paginate(page=page, per_page=2, error_out=False)}
    return render_template('main/index.html', **content)


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/single/<post_id>', methods=['GET', 'POST'])
@cache.memoize(300)
def single(post_id):
    """ article detail """
    post = Post.objects(id=post_id).first()

    post.update(inc__post_views=1)
    if current_user.is_authenticated:
        current_user.add_views_message(post_id, post.title)
    content = {"article": post,
               "comments": post.comments[::-1]}
    return render_template('main/single.html', **content)


@main.route('/add-comment/<post_id>', methods=['POST'])
def add_comment(post_id):
    text = request.form.get("text")
    comment = Comments()
    comment.text = text
    comment.author = User.objects(name=current_user.name).first()
    comment.create_time = datetime.datetime.now()
    Post.objects.get(id=post_id).update(push__comments=comment,
                                        inc__comments_number=1)
    Post.add_messages_user(post_id)
    data = {
        "user_name": current_user.name,
        "user_img_url": url_for('static', filename="img/" + current_user.avatar_img_url),
        "text": text,
        "time": comment.create_time.strftime('%Y-%m-%d %H:%M:%S')}
    return jsonify(data)


@main.route('/search', methods=['POST', 'GET'])
def search():
    """search articles by user' input"""
    keyword = request.args.get('key')

    page = request.args.get('page', 1, type=int)
    content = {
        "articles": Post.search_text(keyword).paginate(page=page, per_page=8, error_out=False)
    }
    return render_template('main/search_result.html', **content)


@main.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    """user add article"""
    form = AddPostForm()
    if form.validate_on_submit():
        form_data = form.data
        title = form_data['title']
        body = form_data['body']
        tags = form_data['get_tags'].split()
        user = User.objects.get(name=current_user.name)
        user.update(inc__post_number=1)
        imag_url = session.pop('POST_IMG', None)
        ok = Post.create(title, body, user, imag_url, tags)
        if ok:
            return redirect(url_for('main.index'))
    return render_template('main/add-post.html', form=form)


@main.route('/upload', methods=['POST', 'GET'])
def upload():
    """user upload image"""
    file = request.files.get('editormd-image-file')
    if not file:
        res = {'success': 0, 'message': '图片格式错误'}
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(Config.POST_IMG_URL,
                               filename).replace('\\', '/'))
        res = {
            'success': 1, 'message': "图片上传成功", 'url': url_for('main.image', name=filename)}
    return jsonify(res)


@main.route('/image/<name>', methods=['GET'])
def image(name=None):
    if name is not None:
        session['POST_IMG'] = name
    with open(os.path.join(Config.POST_IMG_URL, name).replace("\\", '/'), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp


@main.context_processor
@cache.cached(300, key_prefix="hot_article")
def hot_article():
    return dict(hot_article=Post.objects.order_by("-post_views")[:4])
