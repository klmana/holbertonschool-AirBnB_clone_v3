#!/usr/bin/python3
"""return index"""
from api.v1.views import app_views


@app_views.route('/status')
def status_ret():
    """return json"""
    return jsonify({"status": "OK"})
