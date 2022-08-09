from flask_wtf import FlaskForm

from wtforms import (StringField,
                     PasswordField,
                     DateField,
                     SubmitField,
                     EmailField,
                     RadioField,
                     SelectField,
                     TextAreaField)

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


class ProjectForm(FlaskForm):
    name = StringField('Enter the name of the project (it will be changed after agreement):',
                       validators=[Length(max=128)])
    category = SelectField('Choose a category of your project:', choices=[('house', 'House'),
                                                                          ('house reconstruction', 'House reconstruction'),
                                                                          ('commercial building', 'Commercial building'),
                                                                          ('commercial reconstruction', 'Commercial reconstruction')])
    doc_property_rights = RadioField('Documents confirming ownership?', choices=[('Yes', 'Yes'), ('No', 'No')])
    doc_passport = RadioField('Can you bring us your passport?', choices=[('Yes', 'Yes'), ('No', 'No')])
    doc_cadaster =RadioField('Do you have cadastral document?', choices=[('Yes', 'Yes'), ('No', 'No')])
    user_comment = TextAreaField('Leave a additional info here:', validators=[Length(max=256)])
