from flask import jsonify
from flask_security import auth_token_required, current_user
from ..models import User
from . import api
from app import db


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


@api.route('/users/follow/<int:id>', methods=['POST'])
@auth_token_required
def follow(id):

    followed_user = User.query.get(id)  # User.query.filter(User.nickname.ilike(nickname)).first()

    if followed_user is None:
        return jsonify({'errors':[{'message':'No Such User', 'code':600}]})
    if followed_user == current_user:
        return jsonify({'errors':[{'message':'Cannot Follow Yourself', 'code':600}]})

    u = current_user.follow(followed_user)

    if u is None:
        return jsonify({'errors':[{'message':'Already following user', 'code':600}]})

    db.session.add(u)
    db.session.commit()

    return jsonify({'success': followed_user.to_json()})


@api.route('/users/unfollow/<int:id>', methods=['POST'])
@auth_token_required
def unfollow(id):
    unfollowed_user = User.query.get(id)

    if unfollowed_user is None:
        return jsonify({'errors':[{'message':'No Such User', 'code':600}]})
    if unfollowed_user == current_user:
        return jsonify({'errors':[{'message':'Cannot unfollow Yourself', 'code':600}]})

    u = current_user.unfollow(unfollowed_user)

    if u is None:
        return jsonify({'errors':[{'message':'Not following user', 'code':600}]})

    db.session.add(u)
    db.session.commit()

    return jsonify({'success': 'No longer following' + unfollowed_user.nickname})


@api.route('/users/me/', methods=['get'])
@auth_token_required
def get_me():
    user = current_user

    if user is None:
        return jsonify({'user': 'Not Found'})

    return jsonify({'user': user.to_json()})