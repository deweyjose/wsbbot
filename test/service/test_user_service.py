from service.user_service import UserService
from test.service.test_service_base import TestServiceBase
from core.database import db


class TestUserService(TestServiceBase):
    user_svc = UserService()

    def test_create_user_no_commit(self):
        not_committed = self.user_svc.create_user_no_commit("foo", "bar");
        self.assertEqual("foo", not_committed.email)
        db.session.rollback()
        self.assertIsNone(self.user_svc.get_user_by_id(not_committed.id))

    def test_create_user(self):
        created = self.user_svc.create_user("z@z.com", "z")
        self.assertEqual("z@z.com", created.email)
        self.assertIsNone(self.user_svc.create_user("z@z.com", "z"))

    def test_delete_user(self):
        created = self.user_svc.create_user("z@z.com", "z")
        deleted = self.user_svc.delete_user(created.id)
        self.assertEqual(created.id, deleted.id)
        self.assertIsNone(self.user_svc.delete_user(created.id))

    def test_get_user_by_email(self):
        self.user_svc.create_user("z@z.com", "z")
        queried = self.user_svc.get_user_by_email("z@z.com")
        self.assertEqual("z@z.com", queried.email)
        self.assertIsNone(self.user_svc.get_user_by_email("z@za.com"))

    def test_get_user_by_id(self):
        created = self.user_svc.create_user("z@z.com", "z")
        queried = self.user_svc.get_user_by_id(created.id)
        self.assertEqual(created.id, queried.id)
        self.assertIsNone(self.user_svc.get_user_by_id("python"))

    def test_get_all_users(self):
        users = []
        users.append(self.user_svc.create_user("z@z.com", "z"))
        users.append(self.user_svc.create_user("1@1.com", "1"))
        queried = self.user_svc.get_all_users()
        self.assertEqual(len(users), len(queried))

