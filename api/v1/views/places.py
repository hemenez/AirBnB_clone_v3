#!/usr/bin/python3
'''
module for place view
'''
from flask import jsonify, abort, request
from models import storage, classes
import models
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    '''
    function returns all places given a city id
    '''
    places = []
    my_dict = storage.all('Place')
    check_city = storage.get("City", city_id)
    if check_city is None:
        abort(404)
    for k, v in my_dict.items():
        if v.city_id == city_id:
            places.append(v.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def single_place(place_id):
    '''
    function returns a place given its id
    '''
    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''
    function deletes a place given its id
    '''
    to_remove = storage.get("Place", place_id)
    if to_remove is not None:
        storage.delete(to_remove)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    '''
    function creates a new place object given a city id
    '''
    data = request.get_json()
    check_city = storage.get("City", city_id)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif check_city is None:
        abort(404)
    elif 'user_id' not in data:
        return (jsonify({'error': 'Missing user_id'}), 400)
    elif 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)
    check_user = storage.get("User", data['user_id'])
    if check_user is None:
        abort(404)
    else:
        my_new = classes["Place"]()
        for k, v in data.items():
            setattr(my_new, k, v)
        my_new.save()
        return jsonify(my_new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    '''
    function updates a place given its id
    '''
    data = request.get_json()
    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at'\
           and k != 'user_id' and k != 'city_id':
            setattr(my_place, k, v)
    my_place.save()
    return jsonify(my_place.to_dict()), 200
