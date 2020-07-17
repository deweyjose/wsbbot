from unittest import TestCase

from service.user_service import UserService


class TestUserService(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        user_service = UserService(_session=self.session)
        user = user_service.createUser("b@b.com", "b")
        self.assertEqual(user.email, "b@b.com")
        pass

    def test_delete_user(self):
        user = UserService.createUser("b@b.com", "b")
        user = UserService.deleteUser(user.id)
        pass
