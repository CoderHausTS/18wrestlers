# from .. import db
from ..models import Post
from . import api


@api.route('/posts/')
# @login_required
def get_posts():
    # if user.is_anonymous:
    posts = Post.get_all_posts()

    return jsonify({'posts': [post.to_json() for post in posts]})
