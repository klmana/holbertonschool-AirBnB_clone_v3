#!/usr/bin/python3
"""
A view of Place objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def places_all(city_id):
    """Retrieves all Place objects in a particular City"""
    place_objs = storage.get(City, city_id)
    if place_objs is None:
        abort(404)

    list_places = []
    places_dict = storage.all(Place).values()
    for each_place in places_dict:
        if city_id == each_place.city_id:
            list_places.append(each_place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=["GET"],
                 strict_slashes=False)
def place_retrieval(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """Deletes a place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def place_new(city_id):
    """Creates a new Place object"""
    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")
    # request.get_json transforms the HTTP body request to a dict
    id_user = place_data.get("user_id")
    if id_user is None:
        abort(400, "Missing user_id")
    if storage.get(User, id_user) is None:
        abort(404)

    place_name = place_data.get("name")
    if place_name is None:
        abort(400, "Missing name")

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    new_p = Place()
    for key, value in place_data.items():
        setattr(new_p, key, value)
    new_p.city_id = city_id
    storage.new(new_p)
    new_c.save()
    return jsonify(new_p.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")
    for key, value in place_data.items():
        if key not in ignore_list:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
