from flask import Flask
from .api.models import db
from .api import api

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    db.init_app(app)
    api.init_app(app)
    from .api.models import Blog, Author
    with app.app_context():
        db.create_all()

    return app




