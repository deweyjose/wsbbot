"""
Manages Roles, Permissions and RoleNeeds
"""
from flask_principal import Permission, RoleNeed, UserNeed

admin_permission = Permission(RoleNeed('admin'))


class admin_or_me_permission(Permission):
    def __init__(self, user_id):
        super(admin_or_me_permission, self).__init__(RoleNeed('admin'), UserNeed(user_id))
