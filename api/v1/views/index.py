#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

@app_views.route('/status')
def status():
    """return status of our api"""
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def stats():
    """return stats for each column"""
    fullstats = {}
    for key, value in classes.items():
        fullstats[key] = storage.count(value)
    return jsonify(fullstats)
