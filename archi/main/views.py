import datetime
from flask import render_template, redirect, url_for
from flask import current_app as app
from archi.main.forms import RegistrationForm, LoginForm
from ..models import User, Role, db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        reg_date = datetime.datetime.now()
        user = User(name=form.name.data,
                    user_email=form.user_email.data,
                    password=form.password.data,
                    birth_date=form.birthday_date.data,
                    sex=form.sex.data,
                    reg_date=reg_date,
                    role_id='2')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('authpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('authpage.html', form=form)
