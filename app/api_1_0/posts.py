from flask import jsonify, request
from flask_security import auth_token_required
from ..models import Post
from . import api


@api.route('/posts/')
# @login_required
def get_posts():
    posts = Post.get_all_posts()

    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:id>')
@auth_token_required
# @login_required
def get_post(id):
    post = Post.query.get_or_404(id)

    return jsonify({'post': post.to_json()})
