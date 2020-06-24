"""
The User model.
"""
from flask_login import UserMixin

from core.database import db
from core.schemas import ma
from model.role import Role
from model.user_role import UserRole


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    roles = db.relationship('Role', secondary='user_role', lazy='subquery', backref=db.backref('user', lazy=True))


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
