#!/usr/bin/python3
"""This module defines the /cities and /state_id/cities view
"""

from flask import jsonify, abort, request, make_response  # type: ignore
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """retrieves cities object in a state from storage and
    displays JSON representation to it.
    """
    if storage.get(State, state_id) is None:
        abort(404)
    city_list = []
    for key, value in storage.all(City).items():
        if value.state_id == state_id:
            city_list.append(value.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """retrieves city object from storage and
    displays JSON representation to it.
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes city object from storage and displays
    an empty dictionary representation.
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a new city object and adds it to storage
    with the given key value pairs.
    """
    if storage.get(State, state_id) is None:
        abort(404)
    try:
        request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        obj_dict = request.get_json()
        new_city = City(**obj_dict)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a city object with given keys and values
    """
    if storage.get(City, city_id) is None:
        abort(404)
    try:
        request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(City, city_id)
    for key, value in request.get_json().items():
        setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
