#!/usr/bin/python3
"""
  New view for User object that
  handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from models import user
from flask import jsonify
from flask import abort
from flask import request


@app_views.route('/users', methods=["GET"])
def user_get():
    """
      Return json User objects
    """
    users_list = []
    all_users = storage.all("User")
    for user_obj in all_users.values():
        users_list.append(user_obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=["GET"])
def user_get_by_id(user_id):
    """
      Return json State objects by id
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    user_obj = obj.to_dict()
        return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    """
      To delete an object by id
    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=["POST"])
def post_user_obj():
    """
      To add new state object
    """
    dic = {}
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "password" not in dic.keys():
        abort(400, "Missing password")
    if "email" not in dic.keys():
        abort(400, "Missing email")
    new_user = user.User()
    for key, value in dic.items():
        setattr(new_user, key, value)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user_obj(user_id):
    """
      To update new state object
    """
    new_dict = {}
    list_key = ['id', 'email', 'created_at', 'updated_at']
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in list_key:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
