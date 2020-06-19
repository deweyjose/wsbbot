import uuid

from flask import jsonify, request, Blueprint
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from api.exceptions import NotFound, Unauthorized, AlreadyExists
from core.authentication import login_manager
from core.database import db
from model.user import User
from model.user import user_schema, users_schema

user_api = Blueprint('user_api', __name__)


@login_manager.user_loader
def load_user(account_id):
    return User.query.get(account_id)


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, generate_password_hash(password)):
        raise Unauthorized("Unauthorized")
    return True


@user_api.route("/user/register", methods=["GET", "POST"])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        raise AlreadyExists(f"A user has already registered with {email}")

    new_user = User(id=uuid.uuid4(), email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@user_api.route("/user/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise Unauthorized("invalid login")

    login_user(user, remember)

    return jsonify(user_schema.dump(user))


@user_api.route("/user", methods=["GET"])
def get_users():
    all_users = User.query.all()
    return jsonify(users_schema.dump(all_users))


@user_api.route("/user", methods=["POST"])
def create_user():
    user = User(email=request.json['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


@user_api.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if (user == None):
        raise NotFound(f"user {id} not found")
    return jsonify(user_schema.dump(user))


@user_api.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if (user == None):
        raise NotFound(f"user {id} not found")
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))
