#!/usr/bin/python3

from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


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
    if len(states_list) == 0:
        abort(404)
    return jsonify(states_list[0])

@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """delete a state"""
    states_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State" and value.id == state_id:
            states_list.append(value)
    if len(states_list) == 0:
        abort(404)
    storage.delete(states_list[0])
    storage.save()
    return str(states_list[0])

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """create new state"""
    state_json = request.get_json()
    if state_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in state_json:
        return make_response("Missing name", 400)
    new_state = State(**state_json)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(state_json), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def modify_state(state_id):
    """return state object after modification"""
    states_list = []
    state_json = request.get_json()
    if state_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in state_json:
        return make_response("Missing name", 400)
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State" and value.id == state_id:
            states_list.append(value)
    if len(states_list) == 0:
        abort(404)
    for key, value in state_json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            states_list[0].__dict__[key] = value
    storage.save()
    return jsonify(states_list[0].to_dict())
