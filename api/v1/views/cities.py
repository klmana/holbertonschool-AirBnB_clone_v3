#!/usr/bin/python3
"""
A view of City objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def cities_in_state(state_id):
    """Retrieves all City objects in a particular state"""
    state_objs = storage.get(State, state_id)
    if state_objs is None:
        abort(404)

    list_cities = []
    cities_dict = storage.all(City).values()
    for each_city in cities_dict:
        if state_id == each_city.state_id:
            list_cities.append(each_city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def cities_retrieval(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def cities_delete(city_id):
    """Deletes a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def new_city(state_id):
    """Creates a new City object"""
    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, "Not a JSON")
    # request.get_json transforms the HTTP body request to a dict

    city_name = city_data.get("name")
    if city_name is None:
        abort(400, "Missing name")

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    new_c = City()
    for key, value in city_data.items():
        setattr(new_c, key, value)
    new_c.state_id = state_id
    storage.new(new_c)
    new_c.save()
    return jsonify(new_c.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    new_dict = {}
    ignore_list = ["id", "created_at", "updated_at"]
    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, "Not a JSON")
    for key, value in city_data.items():
        if key not in ignore_list:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
