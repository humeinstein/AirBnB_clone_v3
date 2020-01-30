#!/usr/bin/python3
"""create flask view for state objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def get_states():
    """
    GET"/api/v1/states"
    Retrieve State objects:
         Returns jsonify(list)
    def:
    init empty list_of_states []
    - check storage for instances using all.values():
    -- append each instance to empty list_of_states using to_dict {}
    --- jsonify and return list
    """
    list_of_states = []
    for state in storage.all('State').values():
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    GET"api/v1/states/<state_id>"
    Retrieve State by id:
         Returns todict(statefoundbyid)
    else raise 404 error

    def:
    try->
        - check storage for state matching value = state_id
        -- jsonify and return the key: value {'State': state_id}
    error:
        - abort404
    """
    try:
        state = storage.get('State', state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """                                                                                         DELETE "api/v1/states/<state_id>"

    Deletes State obj by id:
        Returns emptry dict with 200 status code
    else raise 404 error

    def:
    try->
        - check storage for state with matching value
        -- try deleting instance
        --- jsonify() and return empty dict with status code 200
    erorr:
        - abort404
    """
    try:
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def post_state():
    """
    POST "api/v1/views/states"


    Creates state
        jsonify and return new instance in dict with 201 status code
    else return Not a JSON or Missing Name (error 400)


    def:
    - check if json request ||return error400 || continue;
    - if name of state does not exit ||return error400 "not a json" || continue;
    - Make State(obj)
    - Save instance
    - jsonify and return new state as dict with success 201
    """
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    new = State(**request.get_json())
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_state(state_id):
    """
    PUT "api/v1/views/states/<state_id>"

    updates state object by id
        setattributes
    return jsonify (state.to_dict())

    def:
    - check if state is in storage to update
    -- abort404 if not state
    -- abort404 if not json
    --- check items of request
    ---- setattributes
    ----- save()
    ------ jsonify and return dict
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
