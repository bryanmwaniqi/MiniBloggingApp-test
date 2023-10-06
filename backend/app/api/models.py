from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates_schema
from flask_jwt_extended import current_user, jwt_required

db = SQLAlchemy()

# SQLAlchemy model classes

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return "Blogpost, {}, posted on {}".format(self.title, self.created_at)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    posts = db.relationship('BlogPost', backref='author')

    def __repr__(self):
        return "User, {} created successfully".format(self.username)

# marshmallow schemas

class BlogSchema(Schema):
    #fields to be validated
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(required=True, dump_only=True)
    author_id = fields.Integer()

    class Meta:
        model = BlogPost

    @validates_schema
    def validate_blogpost(self, data, **kwargs):
        blogpost = BlogPost.query.filter_by(title=data['title']).first()
        if blogpost:
            raise ValidationError('Blogpost with such title already exists')
   
    @post_load
    def make_blogpost(self, data, **kwargs):
        data["author_id"] = current_user.id
        post = BlogPost(**data)
        db.session.add(post)
        db.session.commit()
        return post

class AuthorSchema(Schema):
    #fields to be validated
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(max=50), load_only=True)
    posts = fields.Nested('BlogSchema', exclude=('author_id',), many=True)

    class Meta:
        model = Author

    @validates_schema
    def validate_author(self, data, **kwargs):
        author = Author.query.filter_by(username=data["username"]).first()
        if author:
            raise ValidationError('User with such username already exists')
        
    @post_load
    def make_user(self, data, **kwargs):
        return Author(**data)