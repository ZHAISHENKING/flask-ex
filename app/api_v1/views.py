#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, jsonify, abort, current_app, url_for
from flask.views import MethodView
from app import cache
from app.main.models import Post
from app.public.models import Tags
from app.user.models import User
from . import api_v1
 
class PostViews(MethodView):
    @cache.memoize(300)
    def get(self, post_id=None, user_name=None):
        if user_name:
            try:
                user = User.objects.get(name=user_name)
                posts = Post.objects(author=user)
            except User.DoesNotExist:
                abort(404)

            post_list = {
                'post_number': posts.count(),
                'post_list': [post.to_dict() for post in posts],
            }
        elif post_id:
            post_list = Post.objects.get(id=post_id).to_dict()

        else:
            page = request.args.get('page', 1, type=int)
            pagination = Post.objects.paginate(page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                               error_out=False)
            posts = pagination.items
            prev = None
            if pagination.has_prev:
                prev = url_for('api_v1.post_view', page=page - 1, _external=True)
            next = None
            if pagination.has_next:
                next = url_for('api_v1.post_view', page=page + 1, _external=True)

            post_list = {
                'post_number': pagination.total,
                'post_list': [post.to_dict() for post in posts],
                'prev': prev,
                'next': next
            }
        return jsonify(post_list)

    def post(self):
        abort(405)


class TagsViews(MethodView):
    def get(self, tag_name=None, user_name=None):
        tags_list = None
        if tag_name:
            tag = None
            try:
                tag = Tags.objects.get(name=tag_name)
            except Tags.DoesNotExist:
                abort(404)
            tags_list = tag.to_dict()
        elif user_name:
            try:
                user = User.objects.get(name=user_name)
                tags_list = [tag.to_dict() for tag in user.get_tags]
            except User.DoesNotExist:
                abort(404)
        else:
            tags_list = [ tag.to_dict() for tag in Tags.objects.all()]
        return jsonify(tags_list)


class UserViews(MethodView):
    def get(self, user_name):
        if user_name is None:
            number = User.users_number()
            users_list = {
                'number': number,
                'users_list': [user.to_dict() for user in User.objects],
            }
        else:
            users_list = User.objects.get(name=user_name).to_dict()

        return jsonify(users_list)

    def post(self):
        pass


class UserMessagesVies(MethodView):
    def get(self, user_name):
        user = User.objects.get(name=user_name)

        messages_list = {
            'number': user.messages_number(),
            'messages_list': [mes.to_dict() for mes in user.messages],
        }

        return jsonify(messages_list)


@api_v1.errorhandler(404)
def data_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response


@api_v1.errorhandler(405)
def methods_not_allowed(e):
    response = jsonify({'error': "methods is not allowed"})
    response.status_code = 405
    return response


post_view = PostViews.as_view('post_view')
tags_view = TagsViews.as_view('tags_view')
user_view = UserViews.as_view('user_view')
messages_view = UserMessagesVies.as_view('messages_view')

# post API
api_v1.add_url_rule('/posts/', view_func=post_view, defaults={'post_id': None, 'user_name': None}, methods=['GET'])
api_v1.add_url_rule('/<string:user_name>/post', view_func=post_view, methods=['GET'])
api_v1.add_url_rule('/post/<post_id>', view_func=post_view, methods=['GET'])

# tags API
api_v1.add_url_rule('/tags/', defaults={'tag_name': None, 'user_name': None}, view_func=tags_view)
api_v1.add_url_rule('/tag/<string:tag_name>', view_func=tags_view)
api_v1.add_url_rule('/<string:user_name>/tag', view_func=tags_view)

# users API
api_v1.add_url_rule('/users/', defaults={'user_name': None}, view_func=user_view)
api_v1.add_url_rule('/users/<string:user_name>', view_func=user_view)

# Messages API
api_v1.add_url_rule('/user_mes/<string:user_name>', view_func=messages_view)
