#!/usr/bin/python3
"""Initialize the app_views Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing views
from api.v1.views.index import *
from api.v1.views.states import *  # Import the new states file#!/usr/bin/python3
