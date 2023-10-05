from flask_restful import Resource

class UserRegistration(Resource):
    def post(self):
        pass

class UserLogin(Resource):
    def post(self):
        pass

class Logout(Resource):
    def get(self):
        pass

class Blog(Resource):
    def get(self, id):
        pass

    def Post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

class BlogPosts(Resource):
    def get(self):
        pass
