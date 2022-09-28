import pytest
from archi.models import User, Project
from flask import g
import datetime
from io import BytesIO
import os


def test_register_user(app, client):
    test_data = {'name': 'Slavka_test',
                 'user_email': 'slavka_test@gmail.com',
                 'password': '123123123',
                 'birthday_date': '18/12/1998',
                 'sex': 'female',
                 'submit': 'Submit'}

    response_post = client.post(path='/register',
                                data=test_data,
                                follow_redirects=True)

    assert 'Slavka_test' in response_post.get_data(as_text=True)
    assert len(response_post.history) == 1
    assert response_post.status_code == 200

    test_user = User.get_user_by_name('Slavka_test')
    assert test_user.birthday_date == datetime.date(1998, 12, 18)
    assert g.user.name == test_user.name

    response_post_negative = client.post(path='/register',
                                         data=test_data,
                                         follow_redirects=True)

    assert 'Slavka_test' in response_post_negative.get_data(as_text=True)
    assert 'You already have an account.' in response_post_negative.get_data(as_text=True)


def test_login_and_logout(client, auth):
    auth.login()

    assert g.user.name == User.get_user_by_name('Dzintari').name

    auth.logout()

    response_get = client.get(path='/profile/edit',
                              follow_redirects=True)

    assert g.user is None
    assert 'Login required for this functionality.' in response_get.get_data(as_text=True)


def test_specific_user_page(client, auth):
    auth.login()

    file = (BytesIO(b"abcdef"), '3.jpg')
    test_data = {'photo': file, 'submit': 'Submit'}

    response_post = client.post(path='/users/1',
                                content_type='multipart/form-data',
                                buffered=True,
                                data=test_data,
                                follow_redirects=True)

    assert response_post.status_code == 200

    assert g.user.avatar_path == '3.jpg'

    # deleting mock jpg file
    os.remove(os.path.join(os.getcwd(), 'archi', 'static', 'avatars', '3.jpg'))

    # checking for reassign avatar path
    assert g.user.avatar_path == '1.png'

    auth.logout()


def test_edit_profile(client, auth, projects_mockup):
    auth.login()

    test_data = {'name': 'Dzintari',
                 'birthday_date': '28/12/1911',
                 'sex': 'male',
                 'submit': 'Submit'}

    response_post = client.post(path='/profile/edit',
                                data=test_data,
                                follow_redirects=True)

    assert not User.get_user_by_name('SomeBad_Dzintari')
    new_fixture_user = User.get_user_by_name('Dzintari')

    assert new_fixture_user == g.user
    assert new_fixture_user.birthday_date == datetime.date(1911, 12, 28)

    response_get = client.get('/profile/edit')

    assert 'Enter your name:' in response_get.get_data(as_text=True)
    assert 'Your birthday:' in response_get.get_data(as_text=True)


def test_projects(client, auth, projects_mockup):
    auth.login()

    response_get = client.get(path='/projects',
                              query_string='not_approved_page=2&in_progress_page=1&finished=1&rejected=1')

    assert response_get.status_code == 200
    assert 'Project_for_testing number 4' in response_get.get_data(as_text=True)
    assert 'Project_for_testing number 1' not in response_get.get_data(as_text=True)
    assert 'NonCommercial' not in response_get.get_data(as_text=True)
    assert 'house' in response_get.get_data(as_text=True)

    auth.logout()

    response_get_negative = client.get(path='/projects',
                                       query_string='not_approved_page=1&in_progress_page=1&finished=1&rejected=1',
                                       follow_redirects=True)

    assert 'Login required for this functionality.' in response_get_negative.get_data(as_text=True)


def test_add_project(client, auth, projects_mockup):
    auth.login()
    test_data = {'name': 'Some new project for testing',
                 'category': 'Commercial reconstruction',
                 'doc_property_rights': '1',
                 'doc_passport': '1',
                 'doc_cadaster': '1',
                 'price': '1111',
                 'status': 'Finished',
                 'designer_name': 'Dzintari',
                 'is_approved': 'True',
                 'submit': 'Submit'}

    response_post = client.post(path='/project/add',
                                data=test_data,
                                follow_redirects=True)

    test_project = Project.get_by_name('Some new project for testing')

    assert test_project.name == 'Some new project for testing'
    assert test_project.payments == 0
    assert test_project.designer_id == 1
    assert test_project.user_id == 1
    assert 'Some new project for testing' in response_post.get_data(as_text=True)
    assert 'Project_for_testing number 3' in response_post.get_data(as_text=True)

    response_post_negative = client.post(path='/project/add',
                                         data=test_data,
                                         follow_redirects=True)

    assert 'This name of the project already exists.' in response_post_negative.get_data(as_text=True)

    auth.logout()


def test_edit_project(client, projects_mockup, auth):
    auth.login()

    response_get = client.get(path='/project/edit/1',
                              follow_redirects=True)

    assert response_get.status_code == 200
    assert 'Project_for_testing number 1' in response_get.get_data(as_text=True)

    test_data = {'name': 'Some brand new test name',
                 'category': 'House reconstruction',
                 'status': 'Finished',
                 'is_approved': 'True',
                 'submit': 'Submit'}

    response_post = client.post(path='/project/edit/1',
                                data=test_data,
                                follow_redirects=True)

    assert response_post.status_code == 200
    test_project = Project.get_project_by_id(1, 1)
    assert test_project.name == 'Some brand new test name'
    assert 'Some brand new test name' in response_post.get_data(as_text=True)

    auth.logout()
    auth.login(user_email='slavka_test@gmail.com', password='123123123')

    test_data_1 = {'name': 'Some more new test name',
                 'category': 'House reconstruction',
                 'status': 'Finished',
                 'submit': 'Submit'}

    approved_project_2 = Project.get_project_by_id(2, 2)
    approved_project_2.is_approved = True

    response_post_negative = client.post(path='/project/edit/2',
                                         data=test_data_1,
                                         follow_redirects=True)

    assert 'This project has been approved, you cant edit it.' in response_post_negative.get_data(as_text=True)

    response_post_negative_bad_request = client.post(path='/project/edit/3',
                                                     data=test_data_1,
                                                     follow_redirects=True)

    assert 'Bad request' in response_post_negative_bad_request.get_data(as_text=True)


def test_deleting_project(client, auth, projects_mockup):
    auth.login()

    response_get = client.get(path='/project/delete/1',
                              follow_redirects=True)

    assert response_get.status_code == 200
    assert 'Project deleted.' in response_get.get_data(as_text=True)
    assert not Project.get_project_by_id(1, 1)

    auth.logout()
    auth.login(user_email='slavka_test@gmail.com', password='123123123')

    response_get_negative = client.get('/project/delete/3',
                                       follow_redirects=True)

    assert 'Bad request' in response_get_negative.get_data(as_text=True)

    response_get_negative_2 = client.get('/project/delete/2',
                                       follow_redirects=True)

    assert 'This project has been approved, you cant delete it.' in response_get_negative_2.get_data(as_text=True)
