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


@api.route('/posts/<int:id>')
@auth_token_required
# @login_required
def get_post(id):
    post = Post.query.get_or_404(id)

    return jsonify({'post': post.to_json()})


#
# user = current_user
#
@api.route('/posts/', methods=['POST'])
@auth_token_required
def post():
    if request.method == 'POST':
        post = Post(body=request.json.get('body'), timestamp=datetime.utcnow(), author=current_user)

        db.session.add(post)
        db.session.commit()

    return jsonify({'success': post.to_json()})
