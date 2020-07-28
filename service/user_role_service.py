from core.database import db
from model.role import Role
from model.user_role import UserRole


class UserRoleService:

    def __init__(self, _session=None):
        self.session = _session or db.session

    def create_user_role_no_commit(self, user_id, role_id):
        new_user_role = UserRole(user_id=user_id, role_id=role_id)
        self.session.add(new_user_role)
        return new_user_role

    def create_user_role_by_name(self, user_id, role_name):
        role = Role.query.filter_by(name=role_name).first()
        return self.create_user_role_by_id(user_id, role.id)

    def create_user_role_by_id(self, user_id, role_id):
        new_user_role = self.create_user_role_no_commit(user_id, role_id)
        self.session.commit()
        return new_user_role
