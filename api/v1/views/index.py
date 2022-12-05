#!/usr/bin/python3
"""
A script to create an endpoint that retrieves
the number of objects, for each object, by type
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status_check():
    """Returns an affirmative JSONified status message"""
    text_format = {'status': 'OK'}
    return jsonify(text_format)


@app_views.route('/stats')
def number_of_objects():
    """Displays a count of each object-type"""
    class_count = {}
    for key, class_name in classes.items():
            class_count[key] = storage.count(class_name)
    return jsonify(class_count)
