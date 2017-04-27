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
        output = {'Authentication-Token': user.get_auth_token()}
    else:
        output = {'errors':[{'message':'Bad Authentication Data', 'code':401}]}

    return jsonify(output)

# This is for later. We need to track our logins
#  old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
# old_current_ip, new_current_ip = user.current_login_ip, remote_addr
#
# user.last_login_at = old_current_login or new_current_login
# user.current_login_at = new_current_login
# user.last_login_ip = old_current_ip or new_current_ip
# user.current_login_ip = new_current_ip
# user.login_count = user.login_count + 1 if user.login_count else 1
#
# _datastore.put(user)