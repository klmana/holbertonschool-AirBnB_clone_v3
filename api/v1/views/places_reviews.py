#!/usr/bin/python3
"""
A view of Review objects, handling all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def reviews_all(place_id):
    """Retrieves all Review objects for a particular Place"""

    review_objs = storage.get(Place, place_id)
    if review_objs is None:
        abort(404)
    list_reviews = []
    reviews_dict = storage.all(Review)
    for each_review in reviews_dict.values():
        if each_review.place_id == place_id:
            list_reviews.append(each_review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def review_retrieval(review_id):
    """Retrieves a Review object"""

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """Deletes a Review object"""

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def review_new(place_id):
    """Creates a new Review object"""

    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, "Not a JSON")
    # request.get_json transforms the HTTP body request to a dict
    id_user = review_data.get("user_id")
    if id_user is None:
        abort(400, "Missing user_id")
    if storage.get(User, id_user) is None:
        abort(404)

    id_place = review_data.get("place_id")
    if place_id is None:
        abort(400, "Missing name")

    new_r = Review()
    for key, value in review_data.items():
        if "text" not in review_data.keys():
            abort(400, "Missing text")
        setattr(new_r, key, value)
    new_r.place_id = place_id
    storage.new(new_r)
    new_r.save()
    return jsonify(new_r.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def review_update(review_id):
    """Updates a Review object"""

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    ignore_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ignore_list:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
