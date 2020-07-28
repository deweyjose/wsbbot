from core.database import db
from model.role import Role


class RoleService:
    def __init__(self, _session=None):
        self.session = _session or db.session

    def get_roles(self):
        return Role.query.all()

    def create_role(self, name):
        db.session.add(Role(name=name))
        db.session.commit()
        return Role.query.filter_by(name=name).first()