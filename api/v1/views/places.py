#!/usr/bin/python3

from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('cities/<city_id>/places')
def places(city_id):
    """return place objects linked to a particular city"""
    cities_list = []
    place_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "City" and key.split(".")[1] == city_id:
            cities_list.append(value.to_dict())
    if len(cities_list) == 0:
        abort(404)
    for key1, value1 in response1.items():
        if key1.split(".")[0] == "Place" and value1.city_id == city_id:
            place_list.append(value1.to_dict())
    return jsonify(place_list)

@app_views.route('/places/<place_id>')
def place_id(place_id):
    """return a place based on its id"""
    place_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "place" and value.id == place_id:
            place_list.append(value.to_dict())
    if len(place_list) == 0:
        abort(404)
    return jsonify(place_list[0])

@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """delete a place"""
    place_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "place" and value.id == place_id:
            place_list.append(value)
    if len(place_list) == 0:
        abort(404)
    storage.delete(place_list[0])
    storage.save()
    return str(place_list[0])

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """create new place with given city id"""
    place_json = request.get_json()
    cities_list = []
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "City" and value.id == city_id:
            cities_list.append(value)
    if len(cities_list) == 0:
        abort(404)
    if place_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in place_json:
        return make_response("Missing name", 400)
    place_json['city_id'] = city_id
    new_place = Place(**place_json)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'])
def modify_place(place_id):
    """return city object after modification"""
    place_list = []
    place_json = request.get_json()
    if place_json == None:
        return make_response("Not a JSON", 400)
    if 'name' not in place_json:
        return make_response("Missing name", 400)
    response1 = storage.all()
    for key, value in response1.items():
        if key.split(".")[0] == "place" and value.id == place_id:
            place_list.append(value)
    if len(place_list) == 0:
        abort(404)
    for key, value in place_json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            place_list[0].__dict__[key] = value
    temp_dict = place_list[0].to_dict()
    new_place = Place(**temp_dict)
    storage.delete(place_list[0])
    storage.new(new_place)
    storage.save()
    #return make_response(jsonify({}), 200)
    return make_response(jsonify(place_list[0].to_dict()), 200)
