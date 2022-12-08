#!/usr/bin/python3
"""
A view of Amenity objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"],
                 strict_slashes=False)
def amenities_all():
    """Retrieves all Amenity objects"""
    amenities_dict = storage.all(Amenity).values()
    return jsonify(amenities_dict)


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenity_retrieval(amenity_id):
    """Retrieves an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Deletes an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"],
                 strict_slashes=False)
def new_amenity():
    """Creates a new Amenity object"""
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    if amenity_data.get("name") is None:
        abort(400, "Missing name")
    # request.get_json transforms the HTTP body request to a dict
    new_a = Amenity()
    new_a.name = name
    new_a.save()
    return jsonify(new_a.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    new_dict = {}
    ignore_list = ["id", "created_at", "updated_at"]
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        if key not in ignore_list:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200