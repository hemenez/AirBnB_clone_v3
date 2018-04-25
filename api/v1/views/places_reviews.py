#!/usr/bin/python3
from flask import jsonify, abort, request
from models import storage, classes
import models
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    reviews = []
    for k, v in storage.all('Review').items():
        if v.place_id == place_id:
            reviews.append(v.to_dict())
    if len(reviews) != 0:
        return jsonify(reviews)
    else:
        abort(404)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def single_review(review_id):
    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())

@app_views.route('reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    to_remove = storage.get("Review", review_id)
    if to_remove is not None:
        storage.delete(to_remove)
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    data = request.get_json()
    check_place = storage.get("Place", place_id)
    check_user = storage.get("User", data['user_id'])
    if data is None:
        return (jsonify({'error':'Not a JSON'}), 400)
    elif check_city is None:
        abort(404)
    elif 'user_id' not in data:
        return (jsonify({'error': 'Missing user_id'}), 400)
    elif check_user is None:
        abort(404)
    elif 'text' not in data:
        return (jsonify({'error': 'Text'}), 400)
    else:
        my_new = classes["Review"]()
        setattr(my_new, "place_id", place_id)
        setattr(my_new, "text", data['text'])
        setattr(my_new, "user_id", data['user_id'])
        my_new.save()
        return jsonify(my_new.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    data = request.get_json()
    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    if data is None:
        return (jsonify({'error':'Not a JSON'}), 400)
    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at'\
                             and k != 'user_id' and k != 'place_id':
                             setattr(my_review, k, v)
                             my_review.save()
    return jsonify(my_review.to_dict()), 200
