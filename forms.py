from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length


class RegistrationForm(FlaskForm):
    user_email = StringField('Please, enter a valid email here:', validators=[Email()])
    password = PasswordField('Choose your password:', validators=[Length(min=8, max=12, message='Password must be from 8 to 12 characters.')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_email = StringField('Email:', validators=[Email()])
    password = PasswordField('Password:', validators=[Length(min=8, max=12, message='Password must be from 8 to 12 characters.')])
    submit = SubmitField('Submit')
