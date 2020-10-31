"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional

emailMsg = 'Enter a valid email.'
passMsg = 'Select a password with 6 characters minimum.'
passMatchMsg = 'Passwords must match.'


class SignupForm(FlaskForm):
    """Administrators signup form."""
    name = StringField(
        'Name',
        validators=[InputRequired()])

    email = StringField(
        'Email',
        validators=[Length(min=6),
                    Email(message=emailMsg),
                    InputRequired()])

    password = PasswordField(
        'Password',
        validators=[InputRequired(),
                    Length(min=6, message=passMsg)])

    confirm = PasswordField(
        'Confirm your password',
        validators=[InputRequired(),
                    EqualTo('password', message=passMatchMsg)])

    submit = SubmitField(
        'Register')


class LoginForm(FlaskForm):
    """Administrators login form."""
    email = StringField(
        'Email',
        validators=[InputRequired(),
                    Email(message=emailMsg)])

    password = PasswordField(
        'Password',
        validators=[InputRequired()])

    submit = SubmitField(
        'Log In')
