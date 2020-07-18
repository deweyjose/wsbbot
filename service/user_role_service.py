from core.database import db
from model.role import Role
from model.user_role import UserRole

class UserRoleService:

    def __init__(self, _session=None):
        self.session = _session or db.session

    def assign_investor_role(self, user_id):
        role = Role.query.filter_by(name='investor').first()
        new_user_role = UserRole(user_id=user_id, role_id=role.id)
        self.session.add(new_user_role)
        self.session.commit()
        return new_user_role