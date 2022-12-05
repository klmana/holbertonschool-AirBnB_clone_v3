#!/usr/bin/python3
"""
A script to create an endpoint that retrieves
the number of objects, for each object, by type
"""

from app.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
#classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
#           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status_check():
    """Returns an affirmative JSONified status message"""
    text_format = {
        'status': 'OK'
        }
    return jsonify(text_format)


@app_views.route('/api/v1/stats')
def number_of_objects():
    """Displays a count of each object-type"""
    classes = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
        }
    return jsonify(classes)

#    class_count = {}
#    for each_class in classes.values():
#        class_count.append("{}: {},\n".format(
#            each_class, storage.count(each_class)))
#    return jsonify(class_count)
