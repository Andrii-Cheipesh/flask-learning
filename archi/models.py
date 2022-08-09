from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    birthday_date = db.Column(db.Date)
    sex = db.Column(db.String(32))
    reg_date = db.Column(db.DateTime, default=datetime.datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=2)
    projects = db.relationship('Project', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def get_user_by_email(cls, user_email):
        return cls.query.filter_by(user_email=user_email).first()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    users = db.relationship('User', backref='role')


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(32))
    isapproved = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(32), default='NonCommercial')
    price = db.Column(db.Integer)
    payments = db.Column(db.Integer, default=0)
    doc_property_rights = db.Column(db.Boolean, default=False)
    doc_passport = db.Column(db.Boolean, default=False)
    doc_cadaster = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(32))
    user_comment = db.Column(db.String(256))

    # some date column

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def is_admin_created(self):
        user = User.query.filter_by(id=self.user_id).first()
        if user.role_id == 1:
            return True
