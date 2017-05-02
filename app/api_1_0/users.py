from flask import jsonify
from flask_security import auth_token_required, current_user
from ..models import User
from . import api


@api.route('/users/<int:id>')
@auth_token_required
def get_user(id):
    user = User.query.get(id)

    if user == None:
        return jsonify({'user': 'Not Found'})

    return jsonify({'user': user.to_json()})


@api.route('/users/posts/<int:id>')
@auth_token_required
def get_user_followed_posts(id):
    user = User.query.get(id)
    posts = user.followed_posts()

    return jsonify({'user': user.to_json()}, {'posts': [post.to_json() for post in posts]})


@api.route('/users/follow/<int:id>')
@auth_token_required
def follow(id):

    followed_user = User.query.get(id)

    if not current_user.is_following(followed_user):
        current_user.followed.append(followed_user)
        return jsonify(current_user)
