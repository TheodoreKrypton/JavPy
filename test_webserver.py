# encoding: utf-8

import json
import requests
from JavPy.app.webserver import app
from JavPy.utils.testing import *

app.app.config['TESTING'] = True
client = app.app.test_client()


@testing(code=("ABP-231", "ABP-123", "SSNI-351"))
def test_search_by_code(code):
    rv = client.post('/search_by_code', data=json.dumps({
        'code': code
    }))
    rsp = json.loads(rv.data.decode('utf-8'))
    assert rsp
    assert 'videos' in rsp
    assert len(rsp['videos']) == 1
    assert requests.get(rsp['videos'][0]['video_url']).status_code == 200


@testing(actress=(u"川合まゆ",))
def test_search_by_actress(actress):
    rv = client.post('/search_by_actress', data=json.dumps({
        'actress': actress,
        'history_name': True
    }))
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
    rsp = json.loads(rv.data.decode('utf-8'))
    assert len(rsp) > 0


@testing()
def test_newly_released():
    rv = client.post('/new', data=json.dumps({}))
    rsp = json.loads(rv.data.decode('utf-8'))
    assert len(rsp) > 0


if __name__ == '__main__':
    test_search_by_code()
    test_search_by_actress()
    test_search_magnet_by_code()
    test_newly_released()
