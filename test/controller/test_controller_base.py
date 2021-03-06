from flask_testing import TestCase

import controller
from core.application import app
from core.database import db
from core.schemas import ma


class TestControllerBase(TestCase):

    roles = {}

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testing_secret'

        db.init_app(app)
        ma.init_app(app)

        controller.init_app()
        return app

    def setUp(self):
        from model.role import Role
        db.create_all()
        db.session.add(Role(name='investor'))
        db.session.add(Role(name='admin'))
        db.session.commit()

        r = Role.query.all()

        self.roles = dict( [ (r[i].name,r[i]) for i in range(len(r)) ] )


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, email, password, client, expected_status_code=200):
        """
        helper function to make the test_* methods a bit easier to read
        """
        response = client.post('/register', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        self.assertStatus(response, expected_status_code)

        return response.json

    def login(self, email, password, client, expected_status_code=200):
        """
        helper function to make the test_* methods a bit easier to read
        """
        response = client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        self.assertStatus(response, expected_status_code)

        return response.json

    def logout(self, client, expected_status_code=200):
        """
                helper function to make the test_* methods a bit easier to read
                """
        response = client.get('/logout', follow_redirects=True)

        self.assertStatus(response, expected_status_code)

        return response.json
