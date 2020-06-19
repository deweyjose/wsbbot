from flask_login import UserMixin

from core.database import db
from core.schemas import ma


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    password = db.Column(db.String())
    email = db.Column(db.String(255))


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
