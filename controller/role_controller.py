from flask import Blueprint
from flask import jsonify
from flask_login import login_required

from core.authorization import admin_permission
from model.role import roles_schema
from service.role_service import RoleService

role_api = Blueprint('role_api', __name__)

role_service = RoleService()

@role_api.route("/role", methods=["GET"])
@login_required
@admin_permission.require()
def get_roles():
    roles = role_service.get_roles()
    return jsonify(roles_schema.dump(roles))
