#!/usr/bin/python3
"""Places API view for handling RESTful actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieve all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")
    if 'user_id' not in body:
        abort(400, description="Missing user_id")
    user = storage.get(User, body['user_id'])
    if not user:
        abort(404)
    if 'name' not in body:
        abort(400, description="Missing name")
    body['city_id'] = city_id
    place = Place(**body)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
