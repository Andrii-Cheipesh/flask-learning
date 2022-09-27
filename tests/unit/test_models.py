import pytest
from sqlalchemy.exc import IntegrityError
from flask import g
import datetime
import os

from archi.models import User, Project, db


def test_creation_new_user(app, new_project):
    # GIVEN WHEN THEN
    user_positive = User(name='Slavka',
                         user_email='slavka@gmail.com',
                         password='123123123pass',
                         avatar_path='2.png'
                         )

    db.session.add(user_positive)
    db.session.commit()

    assert user_positive.name == 'Slavka'
    assert user_positive.user_email == 'slavka@gmail.com'
    assert user_positive.role_id == 2

    """user_positive_test.id not 1, because first user
    is automatically created when app is started (__init__.py of archi module)"""
    assert user_positive.id == 2
    assert user_positive.reg_date.strftime("%Y-%m-%d %H:%M") == datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    assert user_positive.avatar_path == '2.png'
    assert not user_positive.avatar_path == '1.png'

    new_project.user_id = user_positive.id
    assert user_positive.ordered_projects.first().id == 1

    with pytest.raises(AttributeError, match='password is not readable attribute'):
        user_positive.password

    assert user_positive.verify_password('123123123pass')
    assert not user_positive.verify_password('wrong_password')

    assert user_positive.get_user_by_name('Slavka') == user_positive

    assert user_positive.get_user_by_email('slavka@gmail.com') == user_positive

    assert user_positive.get_info()['name'] == user_positive.name
    assert user_positive.get_info()['number_of_projects'] == 1


def test_creating_new_user_negative(app, new_project):
    user_negative_1 = User(name='Dzintari',
                         user_email='positive_email@gmail.com',
                         password='123123123pass'
                           )

    with pytest.raises(IntegrityError, match='UNIQUE constraint failed: users.name'):
        db.session.add(user_negative_1)
        db.session.commit()

    db.session.rollback()

    user_negative_2 = User(name='positive_name',
                           user_email='dzintari@gmail.com',
                           password='123123123pass')

    with pytest.raises(IntegrityError, match='UNIQUE constraint failed: users.user_email'):
        db.session.add(user_negative_2)
        db.session.commit()

    db.session.rollback()


def test_creation_new_project_positive(app):
    project = Project(user_id=1,
                      designer_id=1,
                      name='Some test project with unique name',
                      price=3000,
                      payments=2000
                      )

    db.session.add(project)
    db.session.commit()

    assert project.user.id == 1
    assert project.designer.id == 1
    assert project.name == 'Some test project with unique name'
    assert not project.is_approved
    assert project.category == 'NonCommercial'
    assert project.price == 3000
    assert project.payments == 2000
    assert not project.doc_property_rights
    assert not project.doc_passport
    assert not project.doc_cadaster

    assert Project.get_by_name('Some test project with unique name') == project

    with app.app_context():
        g.user = User.get_user_by_name('Dzintari')
        assert Project.get_project_by_id(1, 1)

    assert Project.get_sorted_by_status(User.get_user_by_name('Dzintari').ordered_projects)['not_approved'][0]

    with pytest.raises(IndexError):
        assert Project.get_sorted_by_status(User.get_user_by_name('Dzintari').performed_projects)['in_progress'][0]
        assert Project.get_sorted_by_status(User.get_user_by_name('Dzintari').performed_projects)['finished'][0]
