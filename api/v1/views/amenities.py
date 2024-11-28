#!/usr/bin/python3

from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('amenities/', strict_slashes='False')
def amenities():
    """return amenityty objects linked to a particular state"""
    amenity_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "Amenity":
            amenity_list.append(value.to_dict())
    if len(amenity_list) == 0:
        abort(404)
    return jsonify(amenity_list)

@app_views.route('/amenities/<amenity_id>')
def amenity_id(amenity_id):
    """return a city based on its id"""
    amenity_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "Amenity" and value.id == amenity_id:
            amenity_list.append(value.to_dict())
    if len(amenity_list) == 0:
        abort(404)
    return jsonify(amenity_list[0])

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """delete a city"""
    amenity_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "Amenity" and value.id == amenity_id:
            amenity_list.append(value)
    if len(amenity_list) == 0:
        abort(404)
    storage.delete(amenity_list[0])
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """create new Amenity"""
    amenity_json = request.get_json()
    if amenity_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in amenity_json:
        return make_response("Missing name", 400)
    new_amenity = Amenity(**amenity_json)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def modify_amenity(amenity_id):
    """return amenity object after modification"""
    amenity_list = []
    amenity_json = request.get_json()
    if amenity_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in amenity_json:
        return make_response("Missing name", 400)
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "Amenity" and value.id == amenity_id:
            amenity_list.append(value)
    if len(amenity_list) == 0:
        abort(404)
    for key, value in amenity_json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            amenity_list[0].__dict__[key] = value
    temp_dict = amenity_list[0].to_dict()
    new_amenity = Amenity(**temp_dict)
    storage.delete(amenity_list[0])
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(amenity_list[0].to_dict()), 200)
