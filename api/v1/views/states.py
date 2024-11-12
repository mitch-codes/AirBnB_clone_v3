#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False)
def states():
    """return states objects as a list with all details"""
    states_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State":
            states_list.append(value.to_dict())
    return jsonify(states_list)

@app_views.route('/states/<state_id>')
def states_id(state_id):
    """return states objects as a list with all details"""
    states_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State" and value.id == state_id:
            states_list.append(value.to_dict())
    return jsonify(states_list)
