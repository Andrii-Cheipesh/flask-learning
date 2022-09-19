import pytest

from archi.models import User, db
import datetime


def test_new_user(app, new_project):
    # GIVEN WHEN THEN
    user = User(name='Slavka',
                user_email='slavka@gmail.com',
                password='123123123pass',
                )

    db.session.add(user)
    db.session.commit()

    assert user.name == 'Slavka'
    assert user.user_email == 'slavka@gmail.com'
    assert user.role_id == 2
    # user.id not 1, because first user is automatically created when app is started (__init__.py of archi module)
    assert user.id == 2
    assert user.reg_date.strftime("%Y-%m-%d %H:%M") == datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    assert user.avatar_path == '1.png'

    with pytest.raises(AttributeError):
        user.password

    assert user.verify_password('123123123pass')

    assert User.get_user_by_name('Slavka') == user

    assert User.get_user_by_email('slavka@gmail.com') == user

    new_project.designer_id = user.id
    assert user.performed_projects.first().id == 1
