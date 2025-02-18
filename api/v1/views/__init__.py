#!/usr/bin/python3
"""
Initialize the views module
"""
from flask import Blueprint

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *  # Add this import
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
