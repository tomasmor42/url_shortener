from datetime import datetime
import random
import string
import uuid
from urllib.parse import urljoin

from flask import current_app as app

from .models import db,  Urls

ADDRESS = 'http://' + app.config.get('HOST') + \
    ":" + app.config.get('PORT')  + "/goto/"

ALLOWED_SYMBOLS = string.digits + string.ascii_letters + '_'

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
    now = datetime.utcnow()
    new_entry = Urls(short_url=short_url, full_url=full_url, created=now)
    db.session.add(new_entry)
    db.session.commit()


def validate_shortcode(short_url):
    if len(short_url) != 6:
        return False
    if not all(symbol in ALLOWED_SYMBOLS for symbol in short_url):
        return False
    return True

def is_shortcode_in_use(short_url):
    all_short_urls = [entry.short_url for entry in Urls.query.all()]
    if short_url in all_short_urls:
        return True
    return False

def update_stats(short_url):
    url = Urls.query.filter(Urls.short_url == short_url).first()
    url.last_used = datetime.utcnow()
    url.counts += 1
    db.session.commit()

def get_stats(short_url):
    url = Urls.query.filter(Urls.short_url == short_url).first()
    if url.last_used:
        last_used = url.last_used.isoformat()
    else:
        last_used = None
    stats = {}
    stats['created'] = url.created.isoformat()
    stats['lastRedirect'] = last_used
    stats['redirectCount'] = url.counts
    return stats
