import os
import random
from urllib.parse import urljoin
import uuid
from flask import Flask, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask import current_app as app

from .config import Config
from .models import db,  Urls

ADDRESS = 'http://' + app.config.get('HOST') + ":" + app.config.get('PORT') + "/"

def get_full_url(short_url):
    url = Urls.query.filter(Urls.short_url == short_url).first()
    if not url:
        return None
    full_url = url.full_url
    if full_url is not None:
        if full_url.find("http://") != 0 and full_url.find("https://") != 0:
            full_url = "http://" + full_url
            return full_url
    return full_url

def create_short_url(url):
    len = random.randrange(5, 10)
    url_id = str(uuid.uuid4())[:len]
    return url_id


@app.route("/", methods=['POST'])
def add():
    url = request.form.get('url')
    short_url = create_short_url(url)
    new_entry = Urls(short_url=short_url, full_url=url)
    db.session.add(new_entry)
    db.session.commit()

    return urljoin(ADDRESS+'goto/', short_url), 200


@app.route("/goto/<url>", methods=['GET'])
def main(url):
    full_url = get_full_url(url)
    if not full_url:
        return jsonify({'error':{'message': 'There is no such link'}}), 404 
    return redirect(get_full_url(url))
