from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from core.authentication import login_manager
from core.application import app
from model.user import User


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    # load any other object the user has authorization for here


@login_manager.user_loader
def load_user(user_id):
    """
    used by flask-login to pull the user from the database **if** the user has previously authenticated and is "logged in"
    """
    user = User.query.get(user_id)
    return user