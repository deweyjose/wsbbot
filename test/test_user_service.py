from flask import Flask
from flask_testing import TestCase
from core.database import db
from model.user import User
from service.user_service import UserService

class TestUserService(TestCase):
    user_service = UserService()

    def create_app(self):
        app = Flask(__name__)

        app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TESTING'] = True
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        created = self.user_service.create_user("z@z.com", "z")
        self.assertEqual("z@z.com", created.email)
        self.assertIsNone(self.user_service.create_user("z@z.com", "z"))

    def test_delete_user(self):
        created = self.user_service.create_user("z@z.com", "z")
        deleted = self.user_service.delete_user(created.id)
        self.assertEqual(created.id, deleted.id)
        self.assertIsNone(self.user_service.delete_user(created.id))

    def test_get_user_by_email(self):
        self.user_service.create_user("z@z.com", "z")
        queried = self.user_service.get_user_by_email("z@z.com")
        self.assertEqual("z@z.com", queried.email)
        self.assertIsNone(self.user_service.get_user_by_email("z@za.com"))

    def test_get_user_by_id(self):
        created = self.user_service.create_user("z@z.com", "z")
        queried = self.user_service.get_user_by_id(created.id)
        self.assertEqual(created.id, queried.id)
        self.assertIsNone(self.user_service.get_user_by_id("python"))

    def test_get_all_users(self):
        users = []
        users.append(self.user_service.create_user("z@z.com", "z"))
        users.append(self.user_service.create_user("1@1.com", "1"))
        queried = self.user_service.get_all_users()
        self.assertEqual(len(users), len(queried))
