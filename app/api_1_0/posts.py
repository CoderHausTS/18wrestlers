from flask import jsonify, request
from flask_security import auth_token_required, utils, SQLAlchemyUserDatastore
from ..models import Post, User, Role
from . import api
from app import db

#setup security dude
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


@api.route('/posts/')
@auth_token_required
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



# stolen from flask security.forms.loginform
def verify_login(email, password):


    #  we need to strip if fro the incoming json
    if email.strip() == '':
        # how are we going to send messages
        # email.errors.append(get_message('EMAIL_NOT_PROVIDED')[0])
        return False

    # get this and strip from json
    if password.strip() == '':
        # how are we going to send messages
        # password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
        return False

    user = user_datastore.get_user(email)

    if user is None:
        #email.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
        return False

    if not user.password:
        #password.errors.append(get_message('PASSWORD_NOT_SET')[0])
        return False

    if not utils.verify_and_update_password(password, user):
        #password.errors.append(get_message('INVALID_PASSWORD')[0])
        return False

    if not user.is_active:
        #email.errors.append(get_message('DISABLED_ACCOUNT')[0])
        return False
    #
    return True


@api.route('/auth/', methods=['POST'])
def authenticator():

    # only allow ananymous user
    # get user and validate they exist
    # get username and password from json, set user=("username":username, "password":password)
    #
    # do we use find_user which seems like it's for if you are already logged in    or
    # get_user(email)    user = _datastore.get_user(email.data)
    # from userdatastore? seems like we use get_user
    #
    # if they exist get password and validate passwords match
    # is_active
    # verify_and_update_password(password, user)
    # if the user exists, and the passwords atch, get token
    # get_auth_token

    email = request.json.get('email')
    password = request.json.get('password')

    user_validated = verify_login(email, password)

    if user_validated:
        output = "validated"
    else:
        output = "notvalidaed"

    return jsonify({'output': output})

