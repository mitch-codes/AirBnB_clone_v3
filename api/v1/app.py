#!/usr/bin/python3

from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def tearDown(self):
    """close storage"""
    storage.close()

@app.errorhandler(404)
def handleerror(e):
    """handle 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
