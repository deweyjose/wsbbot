"""
The Role model ;)
"""
from core.database import db
from core.schemas import ma


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role

    id = ma.auto_field()
    name = ma.auto_field()


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
