from service.user_role_service import UserRoleService
from service.user_service import UserService
from test.test_service_base import TestServiceBase
from core.database import db
from model.user_role import UserRole

class TestUserRoleService(TestServiceBase):
    user_svc = UserService()
    user_role_svc = UserRoleService()

    def test_assign_investor_role_no_commit(self):
        user = self.user_svc.create_user_no_commit("z@z.com", "z")
        user_role = self.user_role_svc.assign_investor_role_no_commit(user_id=user.id)
        self.assertEqual(user.id, user_role.user_id)
        db.session.rollback()
        self.assertIsNone(UserRole.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id).first())

    def test_assign_investor_role(self):
        user = self.user_svc.create_user("z@z.com", "z")
        user_role = self.user_role_svc.assign_investor_role(user_id=user.id)
        self.assertEqual(user.id, user_role.user_id)
        self.assertIsNotNone(UserRole.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id).first())
