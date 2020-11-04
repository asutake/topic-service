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

    res = client.get('/topics?sort=-id')

    assert 200 == res.status_code
    assert [
        {
            'id': 3,
            'title': 'タイトル3',
            'created_at': '2022-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 2,
            'title': 'タイトル2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 1,
            'title': 'タイトル1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/topics?offset=1')

    assert 200 == res.status_code
    assert [
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

    res = client.get('/topics?limit=1')

    assert 200 == res.status_code
    assert [
        {
            'id': 1,
            'title': 'タイトル1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/topics?offset=1&limit=1')

    assert 200 == res.status_code
    assert [
        {
            'id': 2,
            'title': 'タイトル2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)


def test_add_topic(client):
    res = client.post(
        '/topics',
        data=json.dumps({
            'title': 'タイトル4',
        }),
        content_type='application/json',
    )

    d = json.loads(res.data)

    assert 201 == res.status_code
    assert 4 == d['id']
    assert 'タイトル4' == d['title']
    assert None != d['created_at']
    assert None == d['deleted_at']

    res = client.get('/topics/4')
    d = json.loads(res.data)

    assert 4 == d['id']
    assert 'タイトル4' == d['title']
    assert None != d['created_at']
    assert None == d['deleted_at']


def test_detail_topic(client):
    res = client.get('/topics/1')

    assert 200 == res.status_code
    assert {
        'id': 1,
        'title': 'タイトル1',
        'created_at': '2020-11-04T19:28:38',
        'deleted_at': None,
    } == json.loads(res.data)


def test_update_topic(client):
    res = client.put(
        '/topics/1',
        data=json.dumps({'title': 'タイトルA'}),
        content_type='application/json',
    )
    assert 200 == res.status_code
    assert {
        'id': 1,
        'title': 'タイトルA',
        'created_at': '2020-11-04T19:28:38',
        'deleted_at': None,
    } == json.loads(res.data)

    res = client.get('/topics/1')

    assert 200 == res.status_code
    assert {
        'id': 1,
        'title': 'タイトルA',
        'created_at': '2020-11-04T19:28:38',
        'deleted_at': None,
    } == json.loads(res.data)


def test_delete_topic(client):
    res = client.delete('/topics/1')

    assert 204 == res.status_code
    assert b'' == res.data

    res = client.get('/topics/1')

    assert 404 == res.status_code
    assert b'404' in res.data


def test_list_comment(client):
    res = client.get('/comments')

    assert 200 == res.status_code
    assert [
        {
            'id': 1,
            'topic_id': 1,
            'text': 'コメント1-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 2,
            'topic_id': 1,
            'text': 'コメント1-2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 3,
            'topic_id': 1,
            'text': 'コメント1-3',
            'created_at': '2022-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 4,
            'topic_id': 2,
            'text': 'コメント2-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/comments?sort=-id')

    assert 200 == res.status_code
    assert [
        {
            'id': 4,
            'topic_id': 2,
            'text': 'コメント2-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 3,
            'topic_id': 1,
            'text': 'コメント1-3',
            'created_at': '2022-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 2,
            'topic_id': 1,
            'text': 'コメント1-2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 1,
            'topic_id': 1,
            'text': 'コメント1-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/comments?offset=1')

    assert 200 == res.status_code
    assert [
        {
            'id': 2,
            'topic_id': 1,
            'text': 'コメント1-2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 3,
            'topic_id': 1,
            'text': 'コメント1-3',
            'created_at': '2022-11-04T19:28:38',
            'deleted_at': None,
        },
        {
            'id': 4,
            'topic_id': 2,
            'text': 'コメント2-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/comments?limit=1')

    assert 200 == res.status_code
    assert [
        {
            'id': 1,
            'topic_id': 1,
            'text': 'コメント1-1',
            'created_at': '2020-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)

    res = client.get('/comments?offset=1&limit=1')

    assert 200 == res.status_code
    assert [
        {
            'id': 2,
            'topic_id': 1,
            'text': 'コメント1-2',
            'created_at': '2021-11-04T19:28:38',
            'deleted_at': None,
        },
    ] == json.loads(res.data)


def test_detail_comment(client):
    res = client.get('/comments/1')

    assert 200 == res.status_code
    assert {
        'id': 1,
        'topic_id': 1,
        'text': 'コメント1-1',
        'created_at': '2020-11-04T19:28:38',
        'deleted_at': None,
    } == json.loads(res.data)
