import pytest
import json

from .. import create_app
from ..api.models import db, AuthorSchema

@pytest.fixture(scope="session")
def client():
    """Instantiate a flask app and initiate a test client """
    app = create_app('config.testing')
    app_ctx = app.app_context()
    app_ctx.push()
    client = app.test_client()
    test_author_data ={
        "username": "pamela",
        "password": "120-pamzo"
    }
    test_author_schema = AuthorSchema()
    test_author = test_author_schema.load(test_author_data)
    db.session.add(test_author)
    db.session.commit()
    yield client
    #Explicit clearing of database & closure of database connection
    db.session.close()
    db.drop_all()
    app_ctx.pop()

