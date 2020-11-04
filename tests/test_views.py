import json


def test_root(client):
    res = client.get('/')

    assert 200 == res.status_code
    assert b'Hello World!' in res.data


def test_list_topic(client):
    res = client.get('/topics')

    assert 200 == res.status_code
    assert [
        {
            'id': 1,
            'title': 'タイトル1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 2,
            'title': 'タイトル2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 3,
            'title': 'タイトル3',
            'created_at': '2022-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)


def test_detail_topic(client):
    res = client.get('/topics/1')

    assert 200 == res.status_code
    assert {
        'id': 1,
        'title': 'タイトル1',
        'created_at': '2020-11-04T19:28:38',
        'deleted_at': None,
    } == json.loads(res.data)
