#!/usr/bin/python3
'''
cities view module
'''
from flask import jsonify, abort, request
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    '''
    function returns all cities given state id
    '''
    cities = []
    check_state = storage.get("State", state_id)
    if check_state is None:
        abort(404)
    for k, v in storage.all('City').items():
        if v.state_id == state_id:
            cities.append(v.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def single_city(city_id):
    '''
    function returns a single city given its id
    '''
    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''
    function deletes a city given its id
    '''
    remove = storage.get("City", city_id)
    if remove is not None:
        storage.delete(remove)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    '''
    function creates new object
    '''
    data = request.get_json()
    check_state = storage.get("State", state_id)
    if check_state is None:
        abort(404)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_inst = classes["City"]()
        setattr(new_inst, "state_id", state_id)
        setattr(new_inst, 'name', data['name'])
        new_inst.save()
        return jsonify(new_inst.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    '''
    function updates city object
    '''
    data = request.get_json()
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
