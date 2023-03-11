import pytest
from archi import create_app
from archi.models import db, User, Role, Project


@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    app.app_context().push()

    yield app

    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture(scope='module')
def projects_mockup(app) -> dict:
    project_1 = Project(user_id=1,
                        designer_id=1,
                        name='Project_for_testing number 1',
                        user_comment='Project_comment number 1'
                        )
    project_2 = Project(user_id=2,
                        designer_id=1,
                        name='Project_for_testing number 2',
                        user_comment='Project_comment number 2'
                        )
    project_3 = Project(user_id=1,
                        designer_id=1,
                        name='Project_for_testing number 3',
                        user_comment='Project_comment number 3'
                        )
    project_4 = Project(user_id=1,
                        designer_id=1,
                        name='Project_for_testing number 4',
                        user_comment='Project_comment number 4',
                        category='house'
                        )
    projects = {'project_1': project_1,
                'project_2': project_2,
                'project_3': project_3,
                'project_4': project_4}

    db.session.add_all([project_1, project_2, project_3, project_4])
    db.session.commit()

    return projects


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, user_email='dzintari@gmail.com', password='123123123'):
        return self._client.post(path='/login',
                                 data={'user_email': user_email, 'password': password},
                                 follow_redirects=True
                                 )

    def logout(self):
        return self._client.get(path='/logout')


@pytest.fixture(scope='function')
def auth(client):
    return AuthActions(client)

    #test for github
