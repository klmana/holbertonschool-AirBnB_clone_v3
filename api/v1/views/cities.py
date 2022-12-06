#!/usr/bin/python3
"""
A view of State objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.city import City
from models.state import State


@app_views.route('/cities', methods=["GET"])
def cities_serialise():
    """Serialises City objects"""
    city_list = []
    city_objs = storage.all("City").values()
    for obj in city_objs:
        city_list.append(obj.to_dict())
    return jsonify(city_list)


@app_views.route('/states/<state_id>/cities', methods=["GET"])
def cities_in_state(state_id):
    """Retrieves all City objects in a particular state"""
    city_objs = storage.get("City", state_id)
    if city_objs is None:
        abort(404)

    return jsonify(city_objs.to_dict())


@app_views.route('/cities/<city_id>', methods=["GET"])
def cities_retrieval(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=["GET"])
def cities_delete(city_id):
    """Deletes a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def new_city(state_id):
    """Creates a new City object"""
    if storage.get(State, state_id) is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    if city_data.get("name") is None:
        abort(400, "Missing name")
    # request.get_json transforms the HTTP body request to a dict
    return jsonify(City.post(city_data, state_id)), 201


@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """Updates a City object"""
    if storage.get(City, city_id) is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    return jsonify(City.put(city_data, city_id)), 200
