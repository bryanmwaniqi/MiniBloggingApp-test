from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates, post_load

db = SQLAlchemy()

# SQLAlchemy model classes

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

# marshmallow schemas

class BlogSchema(Schema):
    #fields to be validated
    title = fields.str(required=True)
    content = fields.str(required=True)
    created_at = fields.Datetime(required=True, dump_only=True)
    author_id = fields.Integer()

    @validates("title")
    def validate_blogpost(self, value):
        blogpost = Blog.query.filter_by(title=value).first()
        if blogpost:
            raise ValidationError('Blogpost with such title already exists')
        
    @post_load
    def make_blogpost(self, data, **kwargs):
        pass

class AuthorSchema(Schema):
    #fields to be validated
    username = fields.str(required=True)
    password = fields.Integer(required=True, load_only=True)
    posts = fields.Nested('BlogSchema', exclude=('author_id',), many=True)

    @validates("username")
    def validate_username(self, value):
        user = Author.query.filter_by(username=value).first()
        if user:
            raise ValidationError('User with such username already exists')
        
    @post_load
    def make_user(self, data, **kwargs):
        return Author(**data)