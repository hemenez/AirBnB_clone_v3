#!/usr/bin/python3
'''
status module
'''
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def response_code():
    '''
    function returns a status response
    '''
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count_objects():
    '''
    function counts how m any objects are in the database
    '''
    count_dict = {}
    count_dict["amenities"] = storage.count("Amenity")
    count_dict["cities"] = storage.count("City")
    count_dict["places"] = storage.count("Place")
    count_dict["reviews"] = storage.count("Review")
    count_dict["states"] = storage.count("State")
    count_dict["users"] = storage.count("User")
    return jsonify(count_dict)
