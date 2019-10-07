import os

from flask import Flask, redirect, request, abort, jsonify, Response
from flask import current_app as app

from .shortener import get_full_url, create_short_url, get_address, store_address

class MissingParameters(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(MissingParameters)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/shorten", methods=['POST'])
def add_api():
    url = request.form.get('url')
    if not url: 
        raise MissingParameters('URL is not present')
    shortcode = request.form.get('shortcode')
    if not shortcode:
        shortcode = create_short_url(url)
        store_address(shortcode, url)
    return jsonify({'url': url, 'shortcode': shortcode}), 201

@app.route("/<url>", methods=['GET'])
def main(url):
    full_url = get_full_url(url)
    if not full_url:
        raise MissingParameters('Shortcode is not present')
    return redirect(get_full_url(url))
