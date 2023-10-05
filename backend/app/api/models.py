from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    author_id = db.column(db.Integer, db.ForeignKey('author.id'), nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(70), nullable=False)
    posts = db.relationship('Blog', backref='author')