#!/usr/bin/python3

from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users/', strict_slashes='False')
def users():
    """return users objects"""
    user_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "User":
            user_list.append(value.to_dict())
    if len(user_list) == 0:
        abort(404)
    return jsonify(user_list)

@app_views.route('/users/<user_id>')
def user_id(user_id):
    """return a users based on its id"""
    user_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "User" and value.id == user_id:
            user_list.append(value.to_dict())
    if len(user_list) == 0:
        abort(404)
    return jsonify(user_list[0])

@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """delete a user"""
    user_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "User" and value.id == user_id:
            user_list.append(value)
    if len(user_list) == 0:
        abort(404)
    storage.delete(user_list[0])
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def add_user():
    """create new Amenity"""
    user_json = request.get_json()
    if user_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in user_json:
        return make_response("Missing name", 400)
    new_user = User(**user_json)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'])
def modify_user(user_id):
    """return amenity object after modification"""
    user_list = []
    user_json = request.get_json()
    if user_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in user_json:
        return make_response("Missing name", 400)
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "User" and value.id == user_id:
            user_list.append(value)
    if len(user_list) == 0:
        abort(404)
    for key, value in user_json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            user_list[0].__dict__[key] = value
    temp_dict = user_list[0].to_dict()
    new_user = User(**temp_dict)
    storage.delete(user_list[0])
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(user_list[0].to_dict()), 200)
