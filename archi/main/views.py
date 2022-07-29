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
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('authpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('authpage.html', form=form)
