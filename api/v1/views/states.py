#!/usr/bin/python3
"""
  View of State object
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=["GET"])
def states_ret():
"""
  Returns json State objects
"""
    state_list = []
    all_objs = storage.all("State")
    for obj in all_objs.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)
