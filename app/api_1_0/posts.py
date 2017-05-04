from flask import jsonify, request, url_for
from flask_security import auth_token_required, current_user
from ..models import Post
from . import api
from app import db
from datetime import datetime


@api.route('/posts/', methods=['GET'])
# @login_required
def get_posts():
    posts = Post.get_all_posts()

    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:id>', methods=['GET'])
@auth_token_required
# @login_required
def get_post(id):
    post = Post.query.get_or_404(id)

    return jsonify({'post': post.to_json()})


#
# post a post, it's the most!
#
@api.route('/posts/', methods=['POST'])
@auth_token_required
def post():
    if request.method == 'POST':
        post = Post(body=request.json.get('body'), timestamp=datetime.utcnow(), author=current_user)

        db.session.add(post)
        db.session.commit()

    return jsonify({'success': post.to_json()})


@api.route('/posts/<int:id>', methods=['DELETE'])
@auth_token_required
def delete(id):
    if request.method == 'DELETE':
        post = Post.query.get(id)

        if post is None:
            return jsonify({'errors': [{'message': 'No Such post', 'code': 600}]})
        if post.author.id != current_user.id:
            return jsonify({'errors': [{'message': 'Unauthorized request', 'code': 600}]})

        db.session.delete(post)
        db.session.commit()

        return jsonify({'status': [{'success': 'Post deleted', 'code': 200}]})


@api.route('/posts/<int:id>', methods=['PATCH'])
@auth_token_required
def post_edit(id):

    if request.method == 'PATCH':

        post = Post.query.get(id)

        if post is None:
            return jsonify({'errors': [{'message': 'No Such post', 'code': 600}]})
        if post.author.id != current_user.id:
            return jsonify({'errors': [{'message': 'Unauthorized request', 'code': 600}]})

        post.body = request.json.get('body')
        post.timestamp = datetime.utcnow()

        db.session.add(post)
        db.session.commit()

        return jsonify({'status': [{'success': 'Post edited', 'code': 200}]})
