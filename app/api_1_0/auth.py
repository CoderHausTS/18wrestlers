from flask import jsonify, request
from flask_security import utils, SQLAlchemyUserDatastore
from ..models import User, Role
from . import api
from app import db


#setup security dude
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# stolen from flask security.forms.loginform
def verify_user(user, password):

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

    email = request.json.get('email')
    password = request.json.get('password')

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

    if verify_user(user, password):
        output = user.get_auth_token()
    else:
        output = ''

    return jsonify({'token': output})

