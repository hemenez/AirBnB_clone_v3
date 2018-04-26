#!/usr/bin/python3
'''
module for user view
'''
from flask import jsonify, abort, request
from models import storage, classes
import models
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def all_users():
    '''
    function returns a list of all user objects
    '''
    my_list = []
    my_dict = storage.all('User')
    for k, v in my_dict.items():
        my_list.append(v.to_dict())
    return jsonify(my_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def single_user(user_id):
    '''
    function returns a single user given its id
    '''
    desired_key = 'User.' + user_id
    my_dict = storage.all('User')
    for k, v in my_dict.items():
        if k == desired_key:
            return jsonify(v.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''
    function deletes a user given its id
    '''
    to_remove = storage.get("User", user_id)
    if to_remove is not None:
        storage.delete(to_remove)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'])
def post_user():
    '''
    function creates a new user object
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in data:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in data:
        return (jsonify({'error': 'Missing password'}), 400)
    else:
        my_new = classes["User"]()
        for k, v in data.items():
            setattr(my_new, k, v)
        my_new.save()
        return jsonify(my_new.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    '''
    function updates a user given a users id
    '''
    data = request.get_json()
    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(my_user, k, v)
    my_user.save()
    return jsonify(my_user.to_dict()), 200
