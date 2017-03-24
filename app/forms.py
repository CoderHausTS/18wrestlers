from wtforms import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_security.forms import RegisterForm
from app import models


class ExtendedRegisterForm(RegisterForm):
    """ Add nickname field to the register's class
    """
    nickname = StringField('Nickname', validators=[DataRequired()])

    def validate(self):
        """ Add nickname validation

            :return: True is the form is valid
        """
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False
        # Check if nickname already exists
        user = models.User.query.filter(
            models.User.nickname.ilike(self.nickname.data)).first()
        if user is not None:
            # Text displayed to the user
            self.nickname.errors.append('Nickname already exists')
            return False

        return True


class EditForm(Form):
    nickname = StringField('nickname', validators=([DataRequired()]))
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, form_data, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        self.form_data = form_data

    def validate_nickname(self):
        """ Add nickname validation

            :return: True is the form is valid
        """

        # Check if nickname already exists
        if self.form_data['nickname'] == self.original_nickname:
            return True
        user = models.User.query.filter(
            models.User.nickname.ilike(self.form_data['nickname'])).first()
        if user is not None:
            # Text displayed to the user
            # some trickery here - as the field errors are a tuple which is immutable.
            tempErrors = list(self.nickname.errors)
            tempErrors.append('User name already in use. Please choose another.')
            self.nickname.errors = tuple(tempErrors)
            return False
        return True


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])
