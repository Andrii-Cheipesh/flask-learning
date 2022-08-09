import functools

from flask import render_template, redirect, url_for, g, session, flash
from flask import current_app as app
from archi.main.forms import RegistrationForm, LoginForm, ProjectForm
from ..models import User, Role, Project, db


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
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not User.get_user_by_name(form.name.data) and not User.get_user_by_email(form.user_email.data):
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            user = User.get_user_by_email(form.user_email.data)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('User with this email or name already exists!')
    return render_template('authpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.user_email.data
        user_password = form.password.data
        user = User.get_user_by_email(user_email)
        if user and user.verify_password(user_password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Incorrect email or password.')
    return render_template('authpage.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/projects')
@login_required
def projects():
    project = Project.get_by_name(name='adminproject')
    if project.is_admin_created():
        project_name = project.name
        user_name = project.user.user_email
        return render_template('projects.html', project_name=project_name, user_name=user_name)
    return redirect(url_for('index'))


@app.route('/project/add')
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        if not Project.get_by_name(form.name.data):
            # some logic for creating project
            return redirect(url_for('projects'))
    return render_template('addproject.html')
