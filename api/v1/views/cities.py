#!/usr/bin/python3
"""
A view of State objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
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
        if state_id == city.state_id:
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


@app_views.route('/cities/<city_id>', methods=["GET"],
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
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    if city_data.get("name") is None:
        abort(400, "Missing name")
    # request.get_json transforms the HTTP body request to a dict
    new_city = City(name=city_data["name"], state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    new_dict = {}
    ignore_list = ["id", "created_at", "updated_at"]
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    for key, value in city_data.items():
        if key not in ignore_list:
            new_dict[key] = value
    city_obj.update(new_dict)
    city_obj.save()
    return jsonify(city.to_dict()), 200
