#!/usr/bin/python3

from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities')
def cities(state_id):
    """return city objects linked to a particular state"""
    states_list = []
    city_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State" and key.split(".")[1] == state_id:
            states_list.append(value.to_dict())
    if len(states_list) == 0:
        abort(404)
    for key1, value1 in response1.items():
        if key1.split(".")[0] == "City" and value1.state_id == state_id:
            city_list.append(value1.to_dict())
    return jsonify(city_list)

@app_views.route('/cities/<city_id>')
def city_id(city_id):
    """return a city based on its id"""
    city_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "City" and value.id == city_id:
            city_list.append(value.to_dict())
    if len(city_list) == 0:
        abort(404)
    return jsonify(city_list[0])

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """delete a city"""
    city_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "City" and value.id == city_id:
            city_list.append(value)
    if len(city_list) == 0:
        abort(404)
    storage.delete(city_list[0])
    storage.save()
    return str(city_list[0])

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """create new city with given state id"""
    city_json = request.get_json()
    states_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "State" and value.id == state_id:
            states_list.append(value)
    if len(states_list) == 0:
        abort(404)
    if city_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in city_json:
        return make_response("Missing name", 400)
    city_json['state_id'] = state_id
    new_city = City(**city_json)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'])
def modify_city(city_id):
    """return state object after modification"""
    city_list = []
    city_json = request.get_json()
    if city_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in city_json:
        return make_response("Missing name", 400)
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "City" and value.id == city_id:
            city_list.append(value)
    if len(city_list) == 0:
        abort(404)
    for key, value in city_json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            city_list[0].__dict__[key] = value
    storage.save()
    return make_response(jsonify({}), 200)
