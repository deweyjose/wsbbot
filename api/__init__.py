"""
API setup
1. Initialize the app, db, schemas and the login_manager
2. Create the principals
3. Register Error Handlers
4. Provide routes for
    - login
    - logout
    - register
    - index
"""

import logging
import os
import random

from flask import Flask, jsonify
from flask_login import current_user
from flask_principal import PermissionDenied, Principal, identity_loaded, UserNeed, RoleNeed

from api.exceptions import AlreadyExists, Unauthorized, NotFound
from api.user_api import user_api
from core.authentication import login_manager
from core.database import db
from core.schemas import ma
from model.user import User

app = Flask("WSBBOT")
app.config.from_object(os.getenv('APP_SETTINGS', 'core.config.DevelopmentConfig'))
db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)

principals = Principal(app)


def wrapp_error(status_code, payload):
    """
    Wrap all of our exception responses in a JSON object
    """
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.errorhandler(Exception)
def handle_unknown(error):
    """
    Catch any unknown exceptions.
    Try to transform errors with a name and code.
    If those attributes do not exist default to 500/unknown error
    """
    logging.error(error)
    return wrapp_error(500 if not hasattr(error, 'code') else error.code,
                       {"message": "unknown error" if not hasattr(error, 'name') else error.name})


@app.errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return wrapp_error(401, {"message": "Permission Denied"})


@app.errorhandler(NotFound)
def handl_not_found(error):
    """
    Catch and transform any NotFound errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())


@app.errorhandler(Unauthorized)
def handle_unauthorized(error):
    """
    Catch and transform any Unauthorized errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())


@app.errorhandler(AlreadyExists)
def handle_already_exists(error):
    """
    Catch and transform any AlreadyExists errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())


@app.route("/", methods=["GET"])
def index():
    """
    The root route. Returns a random popular WSB phrase.
    """
    terms = [
        "Stonks only go up",
        "Pump and dump",
        "All Time High",
        "Due Diligence",
        "It's different this time",
        "Don't fight the fed"
    ]
    return terms[random.randrange(0, len(terms))]


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


app.register_blueprint(user_api)
