#!/usr/bin/python3
"""Reviews API view for handling RESTful actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review for a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")
    if 'user_id' not in body:
        abort(400, description="Missing user_id")
    user = storage.get(User, body['user_id'])
    if not user:
        abort(404)
    if 'text' not in body:
        abort(400, description="Missing text")
    body['place_id'] = place_id
    review = Review(**body)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update an existing Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
