import json
# from app.tests.conftest import register, login, logout

def register(client, username, password):
    resp = client.post('/register',
        data = json.dumps({
            "username": username,
            "password": password
        }), content_type= "application/json")
    return resp

def login(client, username, password):
    return client.post('/login',
    data = json.dumps({
        "username": username,
        "password": password
    }), content_type= "application/json")

def logout(client):
    return client.get('/logout')

def test_get_blogpost(client):
    resp = client.get('/blogposts')
    assert resp.status_code == 200, 'The response status code should be 200'
    assert json.loads(resp.data) == []

def test_update_blogpost(client):
    login_resp = login(client, "pamela", "120-pamzo")
    client.set_cookie("access_token_cookie", json.loads(login_resp.data)["token"])
    resp = client.post('/blogposts',
        data = json.dumps([{
        "title": "A random blogpost",
        "content": "Random blogpost content"
    }]), content_type= "application/json")
    blog_resp = client.put('/blog/1',
                        data = json.dumps({
                        "content": "Random blogpost content update"
                        }), content_type= "application/json")
    assert blog_resp.status_code == 200
    assert json.loads(blog_resp.data)["content"] == "Random blogpost content update"

def test_get_specific_blogpost(client):
    login_resp = login(client, "pamela", "120-pamzo")
    client.set_cookie("access_token_cookie", json.loads(login_resp.data)["token"])
    resp = client.post('/blogposts',
        data = json.dumps([{
        "title": "A random blogpost 2",
        "content": "Random blogpost content"
    }]), content_type= "application/json")
    blog_resp = client.get('/blog/2')
    assert blog_resp.status_code == 200
    assert json.loads(blog_resp.data)["title"] == "A random blogpost 2"
    assert json.loads(blog_resp.data)["content"] == "Random blogpost content"

def test_post_blog(client):
    login_resp = login(client, "pamela", "120-pamzo")
    client.set_cookie("access_token_cookie", json.loads(login_resp.data)["token"])
    resp = client.post('/blogposts',
        data = json.dumps([{
        "title": "Another random blogpost",
        "content": "Random blogpost content"
    }]), content_type= "application/json")
    assert resp.status_code == 201, 'The response status code should be 201'
    assert json.loads(resp.data) == [{
                                        "title": "Another random blogpost",
                                        "content": "Random blogpost content"
                                    }]

def test_registration(client):
    resp = register(client, "kinyua", "kinyua-123")
    assert resp.status_code == 201
    assert json.loads(resp.data) == {"status": "user account kinyua created successfuly"}

def test_login(client):
    resp = login(client, "pamela", "120-pamzo")
    assert resp.status_code == 200
    assert json.loads(resp.data)["status"] == "logged-in"

def test_logout(client):
    login_resp = login(client, "pamela", "120-pamzo")
    client.set_cookie("access_token_cookie", json.loads(login_resp.data)["token"])
    resp = client.get("/logout")
    assert resp.status_code == 200
    assert json.loads(resp.data) == {"status": "logged out successfully"}