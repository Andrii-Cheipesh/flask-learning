from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from archi.models import db, Role, User
    db.init_app(app)

    with app.app_context():
        from archi.main import views
        db.create_all()
        if not Role.query.first():
            admin_role = Role(name='admin')
            user_role = Role(name='user')
            admin_user = User(name='Dzintari', user_email='dzintari@gmail.com', password='123123123', role_id=1)
            db.session.add_all([admin_role, user_role, admin_user])
            db.session.commit()

    return app
