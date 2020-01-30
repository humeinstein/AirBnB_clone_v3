#!/usr/bin/python3
"""create flask view for state objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    GET"/api/v1/states/<state_id>/cities"
    Retrieve city objects:
    Returns jsonify(list)

    def:
    try:
    check if state exists with contents
    init empty list_of_cities []
    - check storage for instances using all.(all->'city'//:
    -- append each instance to empty list_of_cities using to_dict {}
    --- jsonify and return list
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    city_list = []
    cities = storage.all('City').values()
    for city in cities:
        if city.state_id == str(state_id):
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    GET"api/v1/cities/<city_id>"

    Retrieve city by id:
         Returns todict(cityfoundbyid)
    else raise 404 error

    def:
    try->
        - check storage for city matching value = city_id
        -- jsonify and return the key: value {'city': city_id}
    error:
        - abort404
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """
    DELETE "api/v1/cities/<city_id>"

    Deletes city obj by id:
        Returns emptry dict with 200 status code
    else raise 404 error

    def:
    try->
        - check storage for city with matching value
        -- try deleting instance
        --- jsonify() and return empty dict with status code 200
    erorr:
        - abort404
    """
    city = storage.get('City', city_id)
    if city is none:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    POST "api/v1/views/states/<state_id>/cities"


    Creates city
        jsonify and return new instance in dict with 201 status code
    else return Not a JSON or Missing Name (error 400)


    def:
    - check if json request ||return error400 || continue;
    -- if name of city does not exit ||return error400 "not a json" || continue
    --- Make city(obj)
    ---- Save instance
    ----- jsonify and return new state as dict with success 201
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    city = request.get_json()

    if "name" not in city:
        return jsonify({"error": "Missing name"}), 400

    city['state_id'] = state_id
    newcity = City(**city)
    newcity.save()

    return jsonify(newcity.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_city(city_id):
    """
    PUT "api/v1/views/cities/<city_id>"

    updates city object by id
        setattributes
    return jsonify (city.to_dict())

    def:
    - check if state is in storage to update
    -- abort404 if not state
    -- abort404 if not json
    --- check items of request
    ---- setattributes
    ----- save()
    ------ jsonify and return dict
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
