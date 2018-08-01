#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from flask import jsonify

def unauthorized(messages):
    response = jsonify({'error':'unauthorized','message': messages})
    response.status_code = 401
    return response

def forbidden(messages):
    response = jsonify({'error':'forbidden', 'message': messages})
    response.status_code = 403
    return response