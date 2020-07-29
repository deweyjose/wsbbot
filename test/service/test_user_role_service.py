from service.user_role_service import UserRoleService
from service.user_service import UserService
from service.role_service import RoleService
from test.service.test_service_base import TestServiceBase
from core.database import db
from model.user_role import UserRole

class TestUserRoleService(TestServiceBase):
    user_svc = UserService()
    user_role_svc = UserRoleService()
    role_svc = RoleService()

    def test_create_user_role_no_commit(self):
        role_id = self.role_svc.create_role("test").id
        user = self.user_svc.create_user_no_commit("z@z.com", "z")
        user_role = self.user_role_svc.create_user_role_no_commit(user_id=user.id, role_id=role_id)

        self.assertEqual(user.id, user_role.user_id)
        db.session.rollback()
        self.assertIsNone(UserRole.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id).first())

    def test_create_user_role_by_name(self):
        role_id = self.role_svc.create_role("test").id
        user = self.user_svc.create_user("z@z.com", "z")
        user_role = self.user_role_svc.create_user_role_by_name(user_id=user.id, role_name="test")
        self.assertEqual(user.id, user_role.user_id)
        self.assertEqual(role_id, user_role.role_id)
        self.assertIsNotNone(UserRole.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id).first())

    def test_create_user_role_by_id(self):
        role_id = self.role_svc.create_role("test").id
        user = self.user_svc.create_user("z@z.com", "z")
        user_role = self.user_role_svc.create_user_role_by_id(user_id=user.id, role_id=role_id)
        self.assertEqual(user.id, user_role.user_id)
        self.assertEqual(role_id, user_role.role_id)
        self.assertIsNotNone(UserRole.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id).first())

    def test_delete_role_id_for_user_id(self):
        role_id = self.role_svc.create_role("test").id
        user_id = self.user_svc.create_user("z@z.com", "z").id
        user_role = self.user_role_svc.create_user_role_by_id(user_id=user_id, role_id=role_id)

        self.assertEqual(1, len(UserRole.query.filter_by(user_id=user_id).all()))

        deleted = self.user_role_svc.delete_role_id_for_user_id(role_id, user_id)
        self.assertEqual(role_id, deleted.role_id)
        self.assertEqual(user_id, deleted.user_id)
        self.assertEqual(0, len(UserRole.query.filter_by(user_id=user_role.user_id).all()))

        self.assertIsNone(self.user_role_svc.delete_role_id_for_user_id(role_id, user_id))

    def test_delete_user_roles_for_user_id(self):
        role_ids = [self.role_svc.create_role("test").id, self.role_svc.create_role("test2").id]
        user_id = self.user_svc.create_user("z@z.com", "z").id
        for role_id in role_ids:
            self.user_role_svc.create_user_role_by_id(user_id=user_id, role_id=role_id)

        self.assertEqual(2, len(UserRole.query.filter_by(user_id=user_id).all()))
        self.user_role_svc.delete_user_roles_for_user_id(user_id)
        self.assertEqual(0, len(UserRole.query.filter_by(user_id=user_id).all()))


