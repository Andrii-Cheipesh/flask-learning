from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from archi.models import db
    db.init_app(app)

    with app.app_context():
        from archi.main import views
        db.create_all()

    return app
