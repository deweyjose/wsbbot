from core.database import db
from service.user_role_service import UserRoleService
from service.user_service import UserService


class InvestorService:
    user_svc = UserService()
    user_role_svc = UserRoleService()

    def __init__(self, _session=None):
        self.session = _session or db.session

    def create_investor(self, email, password):
        user = self.user_svc.create_user_no_commit(email, password)
        self.user_role_svc.assign_investor_role_no_commit(user.id)
        db.session.commit()
        return self.user_svc.get_user_by_id(user.id)
