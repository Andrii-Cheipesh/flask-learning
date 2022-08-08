from flask_wtf import FlaskForm

from wtforms import (StringField,
                     PasswordField,
                     DateField,
                     SubmitField,
                     EmailField,
                     RadioField)

from wtforms.validators import (Email,
                                Length,
                                InputRequired)


class RegistrationForm(FlaskForm):
    name = StringField('Enter your name:', validators=[InputRequired()])
    user_email = EmailField('Please, enter a valid email here:',
                            validators=[Email()])
    password = PasswordField('Choose your password:',
                             validators=[Length(min=8,
                                                max=12,
                                                message='Password must be from 8 to 12 characters.')])
    birthday_date = DateField('Your birthday:', format='%d/%m/%Y')
    sex = RadioField('Sex:', choices=[('male', 'male'), ('female', 'female')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_email = EmailField('Email:', validators=[Email()])
    password = PasswordField('Password:',
                             validators=[InputRequired()])
    submit = SubmitField('Submit')
