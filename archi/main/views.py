import functools
import os.path

from flask import render_template, redirect, url_for, g, session, flash, request
from flask import current_app as app
from archi.main.forms import RegistrationForm, LoginForm, ProjectForm, EditProjectForm, AvatarForm, ProfileEditForm
from ..models import User, Project, db, UserRole
from werkzeug.utils import secure_filename


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


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users(user_id):
    if g.user.id == user_id:
        form = AvatarForm()
        if form.validate_on_submit():
            file = form.photo.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            g.user.avatar_path = filename
            db.session.commit()

            file.save(file_path)
            return redirect(url_for('users', user_id=user_id))
        user_info = g.user.get_info()
        return render_template('userprofile.html', user_info=user_info, form=form)

    user = User.query.filter_by(id=user_id).first()
    if user:
        user_info = user.get_info()
    else:
        flash('No such user exists.')
        return render_template('user.html')

    return render_template('user.html', user_info=user_info)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_for_edit = g.user
    form = ProfileEditForm(obj=user_for_edit)

    if form.validate_on_submit():
        form.populate_obj(user_for_edit)
        db.session.commit()
        return redirect(url_for('users', user_id=g.user.id))
    return render_template('useredit.html', form=form)


@app.route('/projects')
@login_required
def projects():
    not_approved_page = request.args.get('not_approved_page', default=1, type=int)
    in_progress_page = request.args.get('in_progress_page', default=1, type=int)
    finished_page = request.args.get('finished_page', default=1, type=int)
    rejected_page = request.args.get('rejected_page', default=1, type=int)

    if g.user.role.name == UserRole.user.name:
        projects = g.user.ordered_projects
    else:
        projects = g.user.performed_projects

    sorted_projects = Project.get_sorted_by_status(projects)

    return render_template('projects.html',
                           not_approved=sorted_projects['not_approved'].paginate(not_approved_page, 3, True),
                           in_progress=sorted_projects['in_progress'].paginate(in_progress_page, 3, True),
                           finished=sorted_projects['finished'].paginate(finished_page, 3, True),
                           rejected=sorted_projects['rejected'].paginate(rejected_page, 3, True))


@app.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()

    if form.validate_on_submit():
        if not Project.get_by_name(form.name.data):
            designer = User.get_user_by_name(name=form.designer_name.data)
            project = Project(user_id=g.user.id, designer_id=designer.id)
            form.populate_obj(project)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('projects'))
        flash('This name of the project already exists.')

    return render_template('add_project.html', form=form)


@app.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project_for_edit = Project.get_project_by_id(project_id, g.user.id)
    if not project_for_edit:
        flash('Bad request, 400')
        return redirect(url_for('projects'))

    form = EditProjectForm(obj=project_for_edit)
    if project_for_edit.is_approved and g.user.role.name == UserRole.user.name:
        flash('This project has been approved, you cant edit it.')
        return redirect(url_for('projects'))

    if form.validate_on_submit():
        form.populate_obj(project_for_edit)
        db.session.commit()
        return redirect(url_for('projects'))

    return render_template('projectedit.html', form=form, project_for_edit=project_for_edit)


@app.route('/project/delete/<int:project_id>')
@login_required
def delete_project(project_id):
    project_for_deleting = Project.get_project_by_id(project_id, g.user.id)
    if not project_for_deleting:
        flash('Bad request, 400')

    elif project_for_deleting.is_approved and g.user.role.name == UserRole.user.name:
        flash('This project has been approved, you cant delete it.')

    else:
        db.session.delete(project_for_deleting)
        db.session.commit()
        flash('Project deleted.')
    return redirect(url_for('projects'))
