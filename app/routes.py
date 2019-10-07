import os

from flask import Flask, redirect, request, abort, jsonify, Response
from flask import current_app as app

from .shortener import (get_full_url, create_short_url,
get_address, store_address, validate_shortcode, is_shortcode_in_use,
update_stats, get_stats)

class APIException(Exception):
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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/<url>", methods=['GET'])
def main(url):
    full_url = get_full_url(url)
    if not full_url:
        raise APIException('Shortcode is not present')
    update_stats(url)
    return redirect(get_full_url(url))

@app.route("/<url>/stats", methods=['GET'])
def stats(url):
    if not is_shortcode_in_use(url):
        raise APIException('Shortcode not found')
    return jsonify(get_stats(url))


@app.route("/shorten", methods=['POST'])
def add():
    url = request.form.get('url')
    if not url:
        raise APIException(status_code=400, message='URL is not present')
    shortcode = request.form.get('shortcode')
    if not shortcode:
        shortcode = create_short_url(url)
    else:
        if not validate_shortcode(shortcode):
            raise APIException(
            status_code=412, message='Shortcode is not valid')
        if is_shortcode_in_use(shortcode):
            raise APIException(
            status_code=409, message='Shortcode is already in use')
    store_address(shortcode, url)
    return jsonify({'url': url, 'shortcode': shortcode}), 201
