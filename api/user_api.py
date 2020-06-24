from flask import jsonify, Blueprint
from flask_login import login_required

from api.exceptions import NotFound
from core.database import db
from core.authorization import admin_permission
from model.user import User, user_schema, users_schema

user_api = Blueprint('user_api', __name__)


@user_api.route("/user", methods=["GET"])
@login_required
def get_users():
    all_users = User.query.all()
    return jsonify(users_schema.dump(all_users))


@user_api.route("/user/<id>", methods=["GET"])
@login_required
def get_user(id):
    user = User.query.get(id)
    if (user == None):
        raise NotFound(f"user {id} not found")
    return jsonify(user_schema.dump(user))


@user_api.route("/user/<id>", methods=["DELETE"])
@login_required
@admin_permission.require()
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        raise NotFound(f"user {id} not found")
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))
