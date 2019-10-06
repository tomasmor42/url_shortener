import random
import uuid

import requests
import pytest

def make_url_short(client, post_url):
    res = client.post(
    post_url, data={'url':'www.google.com'})
    return res

def test_create_short_url(client, post_url):
    res = make_url_short(client, post_url)
    assert res.status_code == 200
    url = res.json
    assert url
    assert url.startswith('http://')

def test_check_redirect_url(client, post_url, redirect_url):
    res = make_url_short(client, post_url)
    short_url = res.json
    redirect = client.get(short_url)
    assert redirect.status_code == 302
    