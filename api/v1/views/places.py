#!/usr/bin/python3
"""create flask view for place objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places():
    """ return list of places """
    list_of_places = []
    for place in storage.all('Place').values():
        list_of_places.append(place.to_dict())
    return jsonify(list_of_places)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ return specific place """
    try:
        place = storage.get('Place', place_id)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """ delete specific place """
    try:
        place = storage.get('Place', place_id)
        storage.delete(place)
        storage.save()
        storage.reload()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place():
    """ creates a place """
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Missing Name"})
    if request.json is False:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    new = Place(**request.get_json())
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_place(place_id):
    """ updates a place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
