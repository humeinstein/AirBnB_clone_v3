#!/usr/bin/python3
"""create flask view for state objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ get all amenities """
    users = []
    usercontent = storage.all("User").values()

    for need in usercontent:
        users.append(need.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """
    get user by id
    """
    try:
        users = storage.get('User', user_id)
        return jsonify(users.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """
    delete user by id
    """
    try:
        users = storage.get('User', user_id)
        storage.delete(users)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def post_user():
    """
    post user
    """

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in request.json():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in request.json():
        return jsonify({"error": "Missing password"}), 400
    users = User(
        email=request.get_json(
            ["email"]), password=request.get_json(
            ["password"]))
    userattr = request.get_json().items()
    for key, value in userattr:
        setattr(users, key, value)
    users.save()

    return jsonify(users.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_user(user_id):
    """
    puts user
    """
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    if request.json is False:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(users, key, value)
    users.save()
    return jsonify(user_id.to_dict())
