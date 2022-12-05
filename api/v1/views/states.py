#!/usr/bin/python3
"""
  View of State object and handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify
from flask import abort
from flask import request

def get_state(state):
    """
      Get the state
    """
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()), 200)


def put_state(state):
    """
      Update the state
    """
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    new = request.get_json()
    for (key, value) in new.items():
        if key is not 'id'
        and key is not 'created_at'
        and key is not 'updated_at':
            setattr(state, key, value)
    storage.save()
    return (jsonify(state.to_dict()), 200)


def delete_state(state):
    """
      Delete the state
    """
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """
      Retrieves list of all state objs or creates a state
    """
    if request.method == 'GET':
        all_states = [tmp.to_dict() for tmp in storage.all('State').values()]
        return (jsonify(all_states), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        new = request.get_json()
        if 'name' not in new.keys():
            abort(400, 'Missing name')
        tmp = State()
        for (key, value) in new.items():
            setattr(tmp, key, value)
        tmp.save()
        return (jsonify(tmp.to_dict()), 201)


@app_views.route('/states/<ident>', methods=['GET', 'PUT', 'DELETE'])
def states_id(ident):
    """
      Retrieves a specific state
    """
    states = storage.all('State')
    for s in states.values():
        if s.id == ident:
            if request.method == 'GET':
                return get_state(s)
            elif request.method == 'PUT':
                return put_state(s)
            elif request.method == 'DELETE':
                return delete_state(s)
    abort(404, 'Not found')
