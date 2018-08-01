#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth

from app.user.models import User
from . import api_v1
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.objects.get(email=email_or_token)
    if not user:
        return False
    g.current_user = user

    return user.verify_password(password)


@api_v1.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api_v1.route('/token/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
