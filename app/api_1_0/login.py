from flask import jsonify
from flask_security import UserMixin, datastore, utils

# only allow ananymous user
# get user and validate they exist
# get username and password from json, set user=("username":username, "password":password)
#
# do we use find_user which seems like it's for if you are already logged in    or
# get_user(email)    self.user = _datastore.get_user(self.email.data)
# from userdatastore? seems like we use get_user
#
# if they exist get password and validate passwords match
# is_active
# verify_and_update_password(password, user)
# if the user exists, and the passwords atch, get token
# get_auth_token


# stolen from flask security.forms.loginform
def validate(self, userlogin):


    email = userlogin.email
    password = userlogin.password

    print("email")

    #  we need to strip if fro the incoming json
    if self.email.data.strip() == '':
        # how are we going to send messages
        # self.email.errors.append(get_message('EMAIL_NOT_PROVIDED')[0])
        return False

    # get this and strip from json
    if self.password.data.strip() == '':
        # how are we going to send messages
        # self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
        return False

    self.user = datastore.get_user(self.email.data)

    if self.user is None:
        #self.email.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
        return False
    if not self.user.password:
        #self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
        return False
    if not verify_and_update_password(self.password.data, self.user):
        #self.password.errors.append(get_message('INVALID_PASSWORD')[0])
        return False
    if requires_confirmation(self.user):
        #self.email.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
        return False
    if not self.user.is_active:
        #self.email.errors.append(get_message('DISABLED_ACCOUNT')[0])
        return False
    return True
