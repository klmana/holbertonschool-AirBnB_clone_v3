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
from flask import Flask
from flask import json


@app_views.route('/states', methods=["GET"],
                 strict_slashes=False)
def states_all():
    """Returns all State objects"""
    state_list = []
    all_objs = storage.all("State")
    for obj in all_objs.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=["GET"],
                 strict_slashes=False)
def state_retrieval(state_id):
    """Returns State objects based on id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """Deletes a particular State object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=["POST"],
                 strict_slashes=False)
def state_new():
    """Adds a new State object"""
    state_dict = request.get_json(silent=True)
    if state_dict is None:
        abort(400, "Not a JSON")
    if "name" not in state_dict.keys():
        abort(400, "Missing name")
    new_s = State()
    for key, value in state_dict.items():
        setattr(new_s, key, value)
    storage.new(new_s)
    storage.save()
    return jsonify(new_s.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def state_update(state_id):
    """Updates a State object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    new_dict = {}
    ignore_list = ["id", "created_at", "updated_at"]
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        if key not in ignore_list:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
