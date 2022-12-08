#!/usr/bin/python3
"""The Flask app module"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')

@app.teardown_appcontext
def teardown_appcont(exception):
    """Closes the session currently running"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Returning a message upon encounting a 404 error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")),
            threaded=True, debug=True)
