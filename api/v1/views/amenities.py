#!/usr/bin/python3
"""create flask view for state objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """ get all amenities """

    amenities = []
    amenvalue = storage.all("Amenity").values()

    
    for need in amenvalue:
        amenities.append(need.to_dict())
    return jsonify(amenities)


@app_views.route('/amemities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(city_id):
    """
    get amenity by id
    """
    
    try:
        amen = storage.get('Amenity', amenity_id)
        return jsonify(amen.to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    delete amenity by id
    """
    try:
        amen = storage.get('Amenity', amenity_id)
        storage.delete(amen)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """
    post amenity
    """

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    amenity = request.get_json()

    if "name" not in amenity:
        return jsonify({"error": "Missing name"}), 400

    newamen = Amenity(**amenity)
    newcity.save()

    return jsonify(newamen.to_dict()), 201


@app_views.route('/amenities/<amenitiy_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_amenity(amenity_id):
    """
    puts amenity
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.json is False:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    city.save()
    return jsonify(amenity.to_dict())
