#!/usr/bin/python3
'''
main application module
'''
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)


app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_method(exception):
    '''
    method tears down app
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
    method handles 404 error
    '''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app_host = getenv('HBNB_API_HOST')
    app_port = getenv('HBNB_API_PORT')
    if app_host is None:
        app_host = '0.0.0.0'
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=int(app_port))
