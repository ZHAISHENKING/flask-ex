#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from flask import Blueprint

data = Blueprint('data', __name__)

from . import views