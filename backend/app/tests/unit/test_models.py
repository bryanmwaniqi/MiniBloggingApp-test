import pytest
from flask import current_app
from app.api.models import AuthorSchema, BlogSchema
from marshmallow import ValidationError

def test_new_author(client):
    new_author = {
        "username": "test_user",
        "password": "test_user_pwd"
    }
    test_author_schema = AuthorSchema()
    test_author = test_author_schema.load(new_author)
    resp = test_author_schema.dump(test_author)
    assert resp

def test_new_blog(client):
    new_blog = {
        "title": "test title",
        "post": "test blog content"
    }
    test_blog_schema = BlogSchema()
    with pytest.raises(ValidationError):
        test_blog = test_blog_schema.load(new_blog)

def test_app_client(client):
    assert client
    assert current_app.config["TESTING"] == True