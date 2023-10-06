from flask import Flask
from .api.models import db
from .api.views import jwt
from .api import api

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object('config.config.Default')
    app.config.from_object(config_name)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from .api.models import BlogPost, Author
    with app.app_context():
        db.create_all()

    return app




