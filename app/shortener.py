import uuid
from urllib.parse import urljoin

from flask import current_app as app
import random

#from .config import Config
from .models import db,  Urls


ADDRESS = 'http://' + app.config.get('HOST') + \
    ":" + app.config.get('PORT')  + "/goto/"

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
    url_id = str(uuid.uuid4()).replace('-', '_')[:6]
    return url_id

def get_address(short_url):
    return urljoin(ADDRESS, short_url)

def store_address(short_url, full_url):
    new_entry = Urls(short_url=short_url, full_url=full_url)
    db.session.add(new_entry)
    db.session.commit()
