import uuid

from werkzeug.security import generate_password_hash

from core.database import db
from model.user import User


class UserService:
    def __init__(self, _session=None):
        self.session = _session or db.session

    def getUserByEmail(self, email):
        return User.query.filter_by(email=email).first()

    def getUserById(self, id):
        return User.query.get(id)

    def getAllUsers(self):
        return User.query.all()

    def createUser(self, email, password):
        user = self.getUserByEmail(email)

        if user:
            return None

        user = User(id=str(uuid.uuid4()), email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return user

    def deleteUser(self, id):
        user = self.getUserById(id)
        if user is None:
            return None
        self.session.delete(user)
        self.session.commit()
        return user
