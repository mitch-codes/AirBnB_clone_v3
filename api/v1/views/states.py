#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/states', strict_slashes=False)
def states():
    """return status of our api"""
    states_list = []
    response1 = storage.all()
    for key, value in response1.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)
