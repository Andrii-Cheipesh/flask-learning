import pytest
from archi import create_app
from archi.models import db, User, Role, Project


@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    app.app_context().push()

    yield app

    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture(scope='function')
def new_project(app):
    project = Project(user_id=1,
                      designer_id=1,
                      name='Project_for_testing number 1',
                      user_comment='Project_comment number 1'
                      )
    db.session.add(project)
    db.session.commit()

    return project
