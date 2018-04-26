#!/usr/bin/python3
'''
amenities view module
'''
from flask import jsonify, abort, request
from models import storage, classes
import models
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def all_objects():
    '''
    function returns all amenity objects
    '''
    my_list = []
    my_dict = storage.all('Amenity')
    for k, v in my_dict.items():
        my_list.append(v.to_dict())
    return jsonify(my_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def single_object(amenity_id):
    '''
    function returns single object given its id
    '''
    desired_key = 'Amenity.' + amenity_id
    my_dict = storage.all('Amenity')
    for k, v in my_dict.items():
        if k == desired_key:
            return jsonify(v.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_object(amenity_id):
    '''
    function deletes an object given its id
    '''
    to_remove = storage.get("Amenity", amenity_id)
    if to_remove is not None:
        storage.delete(to_remove)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def post_object():
    '''
    function creates a new amenity object
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)
    else:
        my_new = classes["Amenity"]()
        for k, v in data.items():
            setattr(my_new, k, v)
        my_new.save()
        return jsonify(my_new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_object(amenity_id):
    '''
    function updates an object given its id
    '''
    data = request.get_json()
    my_amenity = storage.get("Amenity", amenity_id)
    if my_amenity is None:
        abort(404)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(my_amenity, k, v)
    my_amenity.save()
    return jsonify(my_amenity.to_dict()), 200
