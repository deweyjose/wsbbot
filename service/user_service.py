import uuid

from werkzeug.security import generate_password_hash

from core.database import db
from model.user import User


class UserService:
    def __init__(self, _session=None):
        self.session = _session or db.session

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_user_by_id(self, id):
        return User.query.get(id)

    def get_all_users(self):
        return User.query.all()

    def create_user_no_commit(self, email, password):
        user = self.get_user_by_email(email)

        if user:
            return None

        user = User(id=str(uuid.uuid4()), email=email, password=generate_password_hash(password))

        db.session.add(user)

        return user

    def create_user(self, email, password):
        user = self.create_user_no_commit(email, password)
        if user:
            db.session.commit()
        return user

    def delete_user(self, id):
        user = self.get_user_by_id(id)
        if user is None:
            return None
        self.session.delete(user)
        self.session.commit()
        return user
