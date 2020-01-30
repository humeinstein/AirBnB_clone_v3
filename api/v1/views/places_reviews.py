#!/usr/bin/python3
"""create flask view for review objects and default restful api actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ returns list of reviews """
    list_of_reviews = []
    place = storage.get('Place', place_id)
    for review in storage.all('Review').values():
        if review.place_id == place_id:
            list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ returns review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """ deletes a review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ creates a review object """

    test_user = storage.get('User', request.json['user_id'])
    if test_user is None:
        abort(404)

    test_place = storage.get('Place', place_id)
    if test_place is None:
        abort(404)

    if 'user_id' not in request.json:
        abort(400)
        return jsonify({"error": "Missing user_id"})

    if 'text' not in request.json:
        abort(400)
        return jsonify({"error": "Missing text"})

    if request.json is False:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    new = Review(**request.get_json())
    storage.save()
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
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
