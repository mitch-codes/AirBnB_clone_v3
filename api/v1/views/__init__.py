#!/usr/bin/python3

from flask import Flask, Blueprint

app_views = Blueprint("views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
