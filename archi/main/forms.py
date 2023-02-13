from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize

from wtforms import (StringField,
                     PasswordField,
                     DateField,
                     SubmitField,
                     EmailField,
                     RadioField,
                     SelectField,
                     TextAreaField,
                     IntegerField,
                     BooleanField)

from wtforms.validators import (Email,
                                Length,
                                InputRequired,
                                NumberRange,
                                Optional,
                                )


class RegistrationForm(FlaskForm):
    name = StringField('Enter your name:', validators=[InputRequired()])
    user_email = EmailField('Please, enter a valid email here:',
                            validators=[Email(), InputRequired()])
    password = PasswordField('Choose your password:',
                             validators=[Length(min=8,
                                                max=12,
                                                message='Password must be from 8 to 12 characters.'),
                                         InputRequired()])
    birthday_date = DateField('Your birthday:', format='%d/%m/%Y', validators=[InputRequired()])
    sex = RadioField('Sex:', choices=[('male', 'male'), ('female', 'female')], validators=[InputRequired()])
    submit = SubmitField('Submit')


class ProfileEditForm(FlaskForm):
    name = StringField('Enter your name:', validators=[InputRequired()])
    birthday_date = DateField('Your birthday:', format='%d/%m/%Y', validators=[InputRequired()])
    sex = RadioField('Sex:', choices=[('male', 'male'), ('female', 'female')], validators=[InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_email = EmailField('Email:', validators=[Email(), InputRequired()])
    password = PasswordField('Password:',
                             validators=[InputRequired()])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    name = StringField('Enter the name of the project (it will be changed after agreement):',
                       validators=[InputRequired(), Length(max=128)])
    category = SelectField('Choose a category of your project:',
                           choices=[('House', 'House'),
                                    ('House reconstruction', 'House reconstruction'),
                                    ('Commercial building', 'Commercial building'),
                                    ('Commercial reconstruction', 'Commercial reconstruction')])
    doc_property_rights = RadioField('Documents confirming ownership?',
                                     coerce=int,
                                     choices=[(1, 'Yes'), (0, 'No')],
                                     validators=[InputRequired()])
    doc_passport = RadioField('Can you bring us your passport?',
                              coerce=int,
                              choices=[(1, 'Yes'), (0, 'No')],
                              validators=[InputRequired()])
    doc_cadaster = RadioField('Do you have cadastral document?',
                              coerce=int,
                              choices=[(1, 'Yes'), (0, 'No')],
                              validators=[InputRequired()])
    user_comment = TextAreaField('Leave a additional info here:',
                                 validators=[Length(max=256)])

    price = IntegerField('Enter the stock price:',
                         validators=[NumberRange(min=0, max=1000000), Optional()])
    payments = IntegerField('Enter the payment amount: ',
                            validators=[NumberRange(min=0, max=1000000), Optional()])
    status = SelectField('Choose a status (NotApproved by default): ',
                         default='NotApproved',
                         choices=[('NotApproved', 'NotApproved'),
                                  ('InProgress', 'InProgress'),
                                  ('Finished', 'Finished'),
                                  ('Rejected', 'Rejected')])
    designer_name = SelectField('Choose a designer:', default='Dzintari',
                                choices=[('Dzintari', 'Dzintari'),
                                         ('Slavka', 'Slavka'),
                                         ('Archi', 'Archi')])

    is_approved = BooleanField('Approve:')

    submit = SubmitField('Create a project')


class EditProjectForm(FlaskForm):
    name = StringField('Enter the name of the project:',
                       validators=[InputRequired(), Length(max=128)])
    category = SelectField('Choose a category of your project:',
                           choices=[('House', 'House'),
                                    ('House reconstruction', 'House reconstruction'),
                                    ('Commercial building', 'Commercial building'),
                                    ('Commercial reconstruction', 'Commercial reconstruction')])
    status = SelectField('Choose a status (NotApproved by default): ',
                         choices=[('NotApproved', 'NotApproved'),
                                  ('InProgress', 'InProgress'),
                                  ('Finished', 'Finished'),
                                  ('Rejected', 'Rejected')])
    is_approved = BooleanField('Approve:')

    submit = SubmitField('Update a project')


class AvatarForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png'], 'Images only!'),
                                  FileSize(max_size=5000000, message='Too big file.')])
