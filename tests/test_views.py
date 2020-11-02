def test_root(client):
    res = client.get('/')

    assert 200 == res.status_code
    assert b'Hello World!' in res.data
