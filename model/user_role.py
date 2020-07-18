"""
The UserRole model
"""

from core.database import db
from core.schemas import ma

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)


class UserRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserRole

    user_id = ma.auto_field()
    role_id = ma.auto_field()


user_role_schema = UserRoleSchema()
user_roles_schema = UserRoleSchema(many=True)

