#!/usr/bin/python3
'''
state view module
'''
from flask import jsonify, abort, request
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def all_states():
    '''
    function returns all state objects
    '''
    return jsonify([v.to_dict() for k, v in storage.all('State').items()])

@app_views.route('/states/<state_id>', methods=['GET'])
def single_state(state_id):
    '''
    function returns state object given its id
    '''
    for k, v in storage.all('State').items():
        if v.id == state_id:
            return jsonify(v.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''
    function deletes an object given its id
    '''
    remove = storage.get("State", state_id)
    if remove is not None:
        storage.delete(remove)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'])
def post_state():
    '''
    function creates a new state object
    '''
    data = request.get_json()
    if data is None:
        return jsonify({'error':'Not a JSON'}), 400
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_inst = classes["State"]()
        setattr(new_inst, 'name', data['name'])
        new_inst.save()
        return jsonify(new_inst.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    '''
    function updates a state object given its id
    '''
    data = request.get_json()
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
