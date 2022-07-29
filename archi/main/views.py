import functools

from flask import render_template, redirect, url_for, g, session, flash
from flask import current_app as app
from archi.main.forms import RegistrationForm, LoginForm
from ..models import User, Role, db


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@app.route('/')
@login_required
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
    if form.validate_on_submit():
        user_email = form.user_email.data
        user_password = form.password.data
        user = User.query.filter_by(user_email=user_email).first()
        if user and user.verify_password(user_password):
            session['user_id'] = user.id
            redirect(url_for('login'))
            return redirect(url_for('login'))
        flash('Incorrect email or password.')
    return render_template('authpage.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
