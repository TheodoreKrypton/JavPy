# encoding: utf-8

from __future__ import unicode_literals, print_function, absolute_import
import json
import requests
from JavPy.app.webserver.app import app, web_dist_path
from JavPy.utils.testing import *
import os

app.config['TESTING'] = True
client = app.test_client()


@testing()
def test_static_files():
    if not os.path.exists(web_dist_path):
        os.mkdir(web_dist_path)
    with open(os.path.join(web_dist_path, "test_index.html"), "w") as fp:
        fp.write("<html></html>")
    rv = client.get('/test_index.html')
    assert rv.status_code == 200
    assert rv.data.decode("utf-8") == "<html></html>"


@testing(code=("ABP-231", "ABP-123", "SSNI-351"))
def test_search_by_code(code):
    rv = client.post('/search_by_code', data=json.dumps({
        'code': code
    }))
    assert rv.status_code == 200
    rsp = json.loads(rv.data.decode('utf-8'))
    assert rsp
    assert 'videos' in rsp
    assert len(rsp['videos']) == 1
    assert requests.get(rsp['videos'][0]['video_url']).status_code == 200


@testing(actress=(u"川合まゆ", u"唯川みさき"))
def test_search_by_actress(actress):
    rv = client.post('/search_by_actress', data=json.dumps({
        'actress': actress,
        'history_name': "true"
    }))
    assert rv.status_code == 200
    rsp = json.loads(rv.data.decode('utf-8'))
    assert rsp
    assert 'other' in rsp
    assert 'history_name' in rsp['other']
    assert len(rsp['other']['history_name']) > 0
    assert 'videos' in rsp
    assert len(rsp['videos']) > 0


@testing(code=("ABP-231", "ABP-123", "SSNI-351"))
def test_search_magnet_by_code(code):
    rv = client.post('/search_magnet_by_code', data=json.dumps({
        'code': code
    }))
    assert rv.status_code == 200
    rsp = json.loads(rv.data.decode('utf-8'))
    assert len(rsp) > 0


@testing(data=({}, {"up_to": 30}, {"page": 1}))
def test_newly_released(data):
    rv = client.post('/new', data=json.dumps(data))
    assert rv.status_code == 200
    rsp = json.loads(rv.data.decode('utf-8'))
    assert len(rsp) > 0


if __name__ == '__main__':
    test_search_by_code()
    test_search_by_actress()
    test_search_magnet_by_code()
    test_newly_released()
