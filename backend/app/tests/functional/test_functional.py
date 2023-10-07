import json


def test_blog(client):
    resp = client.get('/blogposts')
    assert resp.status_code == 200, 'The response status code should be 200'
    assert json.loads(resp.data) == []