#!/usr/bin/python3
"""
start api
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv, environ


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcont(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    hbnb_host = '0.0.0.0'
    hbnb_port = 5000
    if environ.get('HBNB_API_HOST'):
        hbnb_host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        hbnb_port = getenv('HBNB_API_PORT')
