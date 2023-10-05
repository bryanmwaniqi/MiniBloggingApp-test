from .views import (UserRegistration, UserLogin, Logout, Blog, BlogPosts)
from flask_restful import Api

api = Api()

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Blog, '/blog/<int:blog_id>')
api.add_resource(BlogPosts, '/register')