#!/usr/bin/python3
"""API entry point"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for all routes and allow requests from any origin
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors with a JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    from os import getenv
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
