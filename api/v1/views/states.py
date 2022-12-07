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


@app_views.route('/states', methods=["GET"])
def states_get():
    """Return json State object"""
    state_list = []
    all_objs = storage.all("State")
    for obj in all_objs.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=["GET"])
def get_by_id(state_id):
    """
    Return json State objects by id using http verb GET
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"])
def state_delete(state_id):
    """To delete an object by given state_id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=["POST"])
def post_obj():
    """To add new state object"""
    dic = {}
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_state = State()
    for key, value in dic.items():
        setattr(new_state, key, value)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def update_obj(state_id):
    """To update State object"""
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
