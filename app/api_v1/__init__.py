#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint

api_v1 = Blueprint('api_v1',__name__)

from . import views