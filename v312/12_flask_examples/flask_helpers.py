"""
Flask route handler helper.
"""

from flask import jsonify

def setup_routes(app):
    @app.route('/')
    def index():
        return 'Hello from Python + Flask!'

    @app.route('/ping')
    def ping():
        return jsonify({'status': 'ok', 'message': 'Python + Flask is running!'})
