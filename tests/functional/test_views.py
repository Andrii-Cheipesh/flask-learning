import pytest
from archi.models import User
from flask import g
import datetime
from io import BytesIO
import os


def test_index(client):
    response = client.get(path="/")
    assert b'<div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">' in response.data
    assert response.status_code == 200


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
    client.post(path='/users/1',
                content_type='multipart/form-data',
                buffered=True,
                data={'photo': file, 'submit': 'Submit'}
                )

    assert g.user.avatar_path == '3.jpg'

    # deleting mock jpg file
    os.remove(os.path.join(os.getcwd(), 'archi', 'static', 'avatars', '3.jpg'))

    # checking for reassign avatar path
    assert g.user.avatar_path == '1.png'

    auth.logout()
