#!/usr/bin/python3
"""create flask view for review objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews():
    """ returns list of reviews """
    list_of_reviews = {}
    for review in storage.all('Review').values():
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ returns review object """
    try:
        review = storage.get('Review', review_id)
        return jsonify(review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """ deletes a review object """
    try:
        review = storage.get('Review', review_id)
        storage.delete(review)
        storage.save()
        storage.reload()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def post_review():
    """ creates a review object """
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Missing Name"})
    if request.json is False:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    new = Review(**request.get_json())
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def puts_review(review_id):
    """ updates a review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
