from flask import jsonify, request, current_app
from flask_restful import Resource, abort
from marshmallow import ValidationError
from .models import (db, BlogPost, Author, BlogSchema, AuthorSchema)
from flask_jwt_extended import (JWTManager, exceptions, jwt_required, get_jwt, current_user, create_access_token, set_access_cookies, unset_jwt_cookies)

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
    return jwt_payload["jti"] in blocklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"error":"the token has been revoked"}), 401)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        authorschema = AuthorSchema()
        error = authorschema.validate(data)
        if error:
            return jsonify(error)
        new_user = authorschema.load(data)
        db.session.add(new_user)
        db.session.commit()
        resp = jsonify({"status": "user account {} created successfuly".format(new_user.username)})
        resp.status_code = 201
        return resp


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = Author.query.filter_by(username=data['username']).first()
        if not user or user.password != data['password']:
            abort(401, message=("Wrong username or password! Try Again"))
        access_token = create_access_token(identity=user)
        resp = jsonify({"status" : "logged-in", "username": user.username, "token": access_token})
        set_access_cookies(resp, access_token)
        return resp

class Logout(Resource):
    @jwt_required()
    def get(self):
        try:
            jti = get_jwt()["jti"]
            blocklist.add(jti)
        except exceptions.RevokedTokenError as err:
            unset_jwt_cookies(resp)
        resp = jsonify({"status": "logged out successfully"})
        return resp

class Blog(Resource):
    def get(self, blog_id):
        blog = BlogPost.query.filter_by(id=blog_id).first_or_404(description="No blog post with id as {}".format(blog_id))
        blog_schema = BlogSchema()
        resp = blog_schema.dump(blog)
        return resp

    @jwt_required()
    def put(self, blog_id):
        """ Updates only the blogpost content"""
        data = request.get_json()
        blog = BlogPost.query.filter_by(id=blog_id).first()
        if not blog:
            abort(400, message={"error":"No such blogpost"})
        if blog.author_id != current_user.id:
            abort(403, message={"error":"Action forbidden due to non-ownership of blogpost"})
        blog.content = data['content']
        db.session.commit()
        blog_schema = BlogSchema(only=("title", "content"))
        resp = blog_schema.dump(blog)
        return resp

    @jwt_required()
    def delete(self, blog_id):
        blog = BlogPost.query.filter_by(id=blog_id).first()
        
        if not blog:
            abort(400, message={"error":"No such blogpost"})
        if blog.author_id != current_user.id:
            abort(403, message={"error":"Action forbidden due to non-ownership of blogpost"})
        db.session.delete(blog)
        db.session.commit()
        resp = jsonify({"status": "blog post deleted successfully"})
        return resp

class BlogPosts(Resource):
    def get(self):
        all_posts = BlogPost.query.all()
        posts_schema = BlogSchema(many=True)
        resp = posts_schema.dump(all_posts)
        return resp, 200
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        blog_schema = BlogSchema(only=('title', 'content'), many=True)
        error = blog_schema.validate(data)
        if error:
            return jsonify(error)
        try:
            new_posts = blog_schema.load(data)
        except ValidationError as err:
            abort(400, message=err.messages)
        output = blog_schema.dump(new_posts)
        return output, 201
    



