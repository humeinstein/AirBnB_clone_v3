#!/usr/bin/python3
""" creates /status route """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ returns status page """
    dic = {"status": "OK"}
    return jsonify(dic)


@app_views.route('/stats')
def stats():
    """ returns number of objects """
    dic = {}
    classes = {'amenities': 'Amenity',
               'cities': 'City',
               'places': 'Place',
               'reviews': 'Review',
               'states': 'State',
               'users': 'User'}
    for k, v in classes.items():
        dic[k] = storage.count(v)
    return jsonify(dic)
