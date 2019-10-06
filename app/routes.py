import os

from flask import Flask, redirect, request, render_template, jsonify
from flask import current_app as app

from .shortener import get_full_url, create_short_url, get_address, store_address

@app.route("/", methods=['GET'])
def input():
    return render_template('input.html')

@app.route("/", methods=['POST'])
def add_web():
    url = request.form.get('url')
    short_url = create_short_url(url)
    store_address(short_url, url)    
    #import pdb; pdb.set_trace()
    return render_template('input.html', url=get_address(short_url))

@app.route("/api", methods=['POST'])
def add_api():
    url = request.form.get('url')
    short_url = create_short_url(url)
    store_address(short_url, url)    
    return jsonify(get_address(short_url))

@app.route("/goto/<url>", methods=['GET'])
def main(url):
    full_url = get_full_url(url)
    if not full_url:
        return render_template('404.html')
    return redirect(get_full_url(url))
