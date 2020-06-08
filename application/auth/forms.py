"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional

class SignupForm(FlaskForm):
  """Administrators signup form."""
  name = StringField('Name',
                      validators=[InputRequired()])
  email = StringField('Email',
                      validators=[Length(min=6),
                                  Email(message='Enter a valid email.'),
                                  InputRequired()])
  password = PasswordField('Password',
                          validators=[InputRequired(),
                                      Length(min=6, message='Select a password with 6 characters minimum.')])
  confirm = PasswordField('Confirm your password',
                          validators=[InputRequired(),
                          EqualTo('password', message='Passwords must match.')])
  submit = SubmitField('Register')


class LoginForm(FlaskForm):
  """Administrators login form."""
  email = StringField('Email',
                      validators=[InputRequired(),
                      Email(message='Enter a valid email.')])
  password = PasswordField('Password',
                            validators=[InputRequired()])
  submit = SubmitField('Log In')