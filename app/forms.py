# ~\AppData\Local\Programs\Python\Python38\python.exe
# forms.py
__author__ = 'Makias Chaudhary'
__version__ = '1.1'

"""Creates forms for logging in, signing up, sending messages and searching users"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from app import db

# Login form
class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

# Register form
class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    # Custom validation to check if username already in database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken or unavailable')

    # Custom validation to check if email already in database
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email already used or invalid email address')

# Send message form
class SendMessage(FlaskForm):
    body = StringField('Enter your chat here:', validators=[DataRequired()])
    submit = SubmitField('Send')

# User search form
class SearchUser(FlaskForm):
    search = StringField('Search a user to chat with:', validators=[DataRequired()])
    submit = SubmitField('Search')