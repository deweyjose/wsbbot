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
        if not user:
            return None

        # this will commit the transaction for us
        self.user_role_svc.create_user_role_by_name(user_id=user.id, role_name='investor')

        return self.user_svc.get_user_by_id(user.id)
