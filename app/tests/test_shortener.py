import random
import uuid

import requests
import pytest

def make_url_short(client, post_url, url='www.google.com', shortcode=None):
    res = client.post(
    post_url, data={'url':url, 'shortcode':shortcode})
    return res

def test_create_short_url(client, post_url, allowed_symbols):
    res = make_url_short(client, post_url)
    assert res.status_code == 201
    res_dict = res.json
    assert len(res_dict['shortcode']) == 6
    assert all(symbol in allowed_symbols for symbol in res_dict['shortcode'])
    assert res_dict['url'] == 'www.google.com'

def test_create_short_url_with_shortcode(client, post_url):
    res = make_url_short(client, post_url, shortcode='1q2w3e')
    assert res.status_code == 201
    res_dict = res.json
    assert res_dict['shortcode'] == '1q2w3e'
    assert res_dict['url'] == 'www.google.com'

def test_invalid_shortcode(client, post_url):
    res = make_url_short(client, post_url, shortcode='!Q@W#E')
    assert res.status_code == 412

def test_existing_shortcode(client, post_url):
    make_url_short(client, post_url, shortcode='2w3e4r')
    res = make_url_short(client, post_url, shortcode='2w3e4r')
    assert res.status_code == 409

def test_check_redirect_url(client, post_url, redirect_url):
    res = make_url_short(client, post_url)
    short_url = res.json['shortcode']
    redirect = client.get(short_url)
    assert redirect.status_code == 302

def test_check_redirect_not_exist_url(client, post_url, redirect_url):
    short_url = '12345'
    redirect = client.get(short_url)
    assert redirect.status_code == 404

def test_stats_empty(client, post_url, redirect_url):
    res = make_url_short(client, post_url)
    short_url = res.json['shortcode']
    stats = client.get(short_url+'/stats')
    assert stats.status_code == 200
    assert not stats.json['lastRedirect']
    assert stats.json['redirectCount'] == 0
    assert stats.json['created']

def test_stats_not_empty(client, post_url, redirect_url):
    res = make_url_short(client, post_url)
    short_url = res.json['shortcode']
    client.get(short_url)
    stats = client.get(short_url+'/stats')
    assert stats.status_code == 200
    assert stats.json['lastRedirect']
    assert stats.json['redirectCount'] == 1
    assert stats.json['created']

def test_stats_doesnt_exist(client, post_url):
    short_url = '5t6y7u'
    stats = client.get(short_url+'/stats')
    assert stats.status_code == 404
