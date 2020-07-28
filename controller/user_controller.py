from flask import Blueprint
from flask import request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from werkzeug.security import check_password_hash

from controller.exceptions import NotFound, Unauthorized, AlreadyExists
from core.authorization import admin_permission
from model.user import user_schema, users_schema
from model.user_role import user_role_schema
from service.investor_service import InvestorService
from service.user_role_service import UserRoleService
from service.user_service import UserService

user_api = Blueprint('user_api', __name__)

user_service = UserService()
investor_service = InvestorService()
user_role_service = UserRoleService()


@user_api.route('/user/<user_id>/roles/<role_id>', methods=['PUT'])
@login_required
@admin_permission.require()
def grant_role_to_user(user_id, role_id):
    """
    Grant the role to the user. Must be admin
    """
    new_user_role = user_role_service.create_user_role_by_id(user_id=user_id, role_id=role_id)
    return jsonify(user_role_schema.dump(new_user_role))


@user_api.route("/user", methods=["GET"])
@login_required
@admin_permission.require()
def get_users():
    """
    Get a list of all users. must be admin.
    todo: paging support
    """
    all_users = user_service.get_all_users()
    return jsonify(users_schema.dump(all_users))


@user_api.route("/user/<id>", methods=["GET"])
@login_required
def get_user(id):
    """
    Get the user: must be admin or logged in user
    """
    if admin_permission.can() or current_user.id == id:
        user = user_service.get_user_by_id(id)
        if (user == None):
            raise NotFound(f"user {id} not found")
        return jsonify(user_schema.dump(user))
    else:
        raise Unauthorized("Unauthorized")


@user_api.route("/user/<id>", methods=["DELETE"])
@login_required
def delete_user(id):
    """
    Delete the user: must be admin or logged in user
    """
    if admin_permission.can() or current_user.id == id:
        user = user_service.delete_user(id)
        if user is None:
            raise NotFound(f"user {id} not found")
        return jsonify(user_schema.dump(user))
    else:
        raise Unauthorized("Unauthorized")


def authenticate_user(email, password):
    """
    Authenticate the User:
        1. Fetch the user from the database
        2. Make sure the password hashes match
    """
    user = user_service.get_user_by_email(email)

    if user is None or not check_password_hash(user.password, password):
        raise Unauthorized("Unauthorized")

    return user


@user_api.route("/login", methods=["POST"])
def login():
    """
    Login route:
    1. authenticate the user
    2. login_user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember', False)

    user = authenticate_user(email, password)

    login_user(user, remember)

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    return jsonify(user_schema.dump(user))


@user_api.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Log the user out so session state is cleared.
    """
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return jsonify({"messaged": "logged out"})


@user_api.route("/register", methods=["GET", "POST"])
def register_user():
    """
    Register the user. assign investor role by default
    """
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = investor_service.create_investor(email, password)

    if new_user == None:
        raise AlreadyExists("An account with that email address already exists")

    return jsonify(user_schema.dump(user_service.get_user_by_id(new_user.id)))
