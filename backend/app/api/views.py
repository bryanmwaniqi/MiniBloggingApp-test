from flask import jsonify, request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from .models import (db, Blog, Author, BlogSchema, AuthorSchema)
from flask_jwt_extended import (JWTManager, jwt_required, current_user, create_access_token)

jwt = JWTManager()
blocklist = set()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Author.query.filter_by(username=identity).one_or_none()

@jwt.token_in_blocklist_loader
def check_if_token_blocklist(jwt_header, jwt_payload):
    jti = jwt["jti"]
    return jti in blocklist

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        authorschema = AuthorSchema()
        error = authorschema.validate(data)
        if error:
            return jsonify(error)
        new_user = authorschema.load(data)
        db.session.add(new_user)
        new_user_schema = AuthorSchema(only=(['username']))
        output = new_user_schema.dump(new_user)
        return output, 201


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = Author.query.filter_by(username=data['username']).first()
        if not user or user.password != data['password']:
            abort(401, message=("Wrong username or password! Try Again"))
        access_token = create_access_token(identity=user)
        resp = jsonify({"status" : "logged-in", "username": user.username})
        return resp

class Logout(Resource):
    @jwt_required
    def get(self):
        resp = jsonify({"logout status": "True"})
        resp.status_code = 200
        return resp

class Blog(Resource):
    def get(self, blog_id):
        blog = Blog.query.filter_by(id=blog_id).first_or_404(description="No blog post with {}".format(blog_id))
        blog_schema = BlogSchema()
        resp = blog_schema.dump(blog)
        return resp

    @jwt_required
    def Post(self):
        data = request.get_json()
        blog_schema = BlogSchema()
        error = blog_schema.validate(data)
        if error:
            abort(400, message=error)
        try:
            new_posts = blog_schema.load(data)
        except ValidationError as err:
            abort(400, message=err.messages)

    @jwt_required
    def put(self, blog_id):
        """ Updates only the blogpost content"""
        data = request.get_json()
        blog = Blog.query.filter_by(id=blog_id).first()
        if not blog:
            abort(400, message={"error":"No such blogpost"})
        if blog.author_id != current_user.id:
            abort(403, message={"error":"Action forbidden due to non-ownership of blogpost"})
        blog.content = data.content
        db.session.commit()
        blog_schema = BlogSchema()
        resp = blog_schema.dump(blog)

    @jwt_required
    def delete(self, blog_id):
        blog = Blog.query.filter_by(id=blog_id).first()
        if not blog:
            abort(400, message={"error":"No such blogpost"})
        if blog.author_id != current_user.id:
            abort(403, message={"error":"Action forbidden due to non-ownership of blogpost"})
        db.session.delete(blog)
        db.session()

class BlogPosts(Resource):
    def get(self):
        all_posts = Blog.query.all()
        posts_schema = BlogSchema(many=True)
        resp = posts_schema.dump(all_posts)
        return resp, 200
