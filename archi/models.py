from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import g
from enum import Enum

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
    avatar_path = db.Column(db.String, default=r'1.png')
    ordered_projects = db.relationship("Project", foreign_keys='[Project.user_id]', back_populates='user', lazy='dynamic')
    performed_projects = db.relationship("Project", foreign_keys='[Project.designer_id]', back_populates='designer', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_user_by_email(cls, user_email):
        return cls.query.filter_by(user_email=user_email).first()

    def get_info(self) -> dict:
        user_info = {
            'name': self.name,
            'user_email': self.user_email,
            'birthday_date': self.birthday_date,
            'sex': self.sex,
            'reg_date': self.reg_date,
            'role': self.role.name,
            'number_of_projects': (
                len(self.performed_projects.all()) if self.role.name == UserRole.admin.name
                else len(self.ordered_projects.all())),
            'avatar_path': self.avatar_path
        }
        return user_info


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    users = db.relationship('User', backref='role')


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    designer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys="[Project.user_id]", back_populates='ordered_projects')
    designer = db.relationship("User", foreign_keys="[Project.designer_id]", back_populates='performed_projects')

    name = db.Column(db.String(32), unique=True)
    is_approved = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(32), default='NonCommercial')
    price = db.Column(db.Integer, default=0)
    payments = db.Column(db.Integer, default=0)
    doc_property_rights = db.Column(db.Boolean, default=False)
    doc_passport = db.Column(db.Boolean, default=False)
    doc_cadaster = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(32), default='NotApproved')
    user_comment = db.Column(db.String(256))

    # some date column

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_project_by_id(cls, id, user_id):
        if g.user.role.name == 'admin':
            return Project.query.filter_by(id=id).first()
        return Project.query.filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def get_sorted_by_status(projects) -> dict:
        not_approved = projects.filter_by(status='NotApproved')
        in_progress = projects.filter_by(status='InProgress')
        finished = projects.filter_by(status='Finished')
        rejected = projects.filter_by(status='Rejected')

        return {'not_approved': not_approved, 'in_progress': in_progress, 'finished': finished, 'rejected': rejected}


class UserRole(Enum):
    admin = 'admin'
    user = 'user'
