from flask import Flask
from flask_testing import TestCase

from core.database import db


class TestServiceBase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TESTING'] = True
        db.init_app(app)
        return app

    def setUp(self):
        from model.role import Role
        db.create_all()
        role = Role(name='investor')
        db.session.add(role)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
