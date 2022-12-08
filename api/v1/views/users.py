#!/usr/bin/python3
"""New view for User object"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET"],
                 strict_slashes=False)
def all_users():
    """Returns all User objects"""

    list_users = []
    user_dict = storage.all(User)
    for each_user in user_dict.values():
        list_users.append(each_user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def user_retrieval(user_id):
    """Returns a particular User object by id"""

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def user_delete(user_id=None):
    """Deletes a User object"""

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"],
                 strict_slashes=False)
def user_add():
    """Adds a new User object"""

    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    new_u = User()
    for key, value in user_data.items():
        if "password" not in user_data.keys():
            abort(400, "Missing password")
        if "email" not in user_data.keys():
            abort(400, "Missing email")
        setattr(new_u, key, value)
    storage.new(new_u)
    new_u.save()
    return jsonify(new_u.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user_obj(user_id=None):
    """To update new state object"""

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    ignore_list = ["id", "email", "created_at", "updated_at"]
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ignore_list:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
