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
import uuid

from flask import Flask, request, jsonify
from flask_login import login_user, logout_user, login_required
from flask_principal import Principal
from werkzeug.security import generate_password_hash, check_password_hash

from api.exceptions import AlreadyExists, Unauthorized, NotFound
from api.user_api import user_api
from core.authentication import login_manager
from core.database import db
from core.schemas import ma
from model.user import User, user_schema

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
    logging.debug(error)
    return wrapp_error(500 if not error.code else error.code,
                       {"message": "unknown error" if not error.name else error.name})


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


def authenticate_user(email, password):
    """
    Authenticate the User:
        1. Fetch the user from the database
        2. Make sure the password hashes match
    """
    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        raise Unauthorized("Unauthorized")

    return user


@login_manager.user_loader
def load_user(user_id):
    """
    used by flask-login to pull the user from the database **if** the user has previously authenticated and is "logged in"
    """
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
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

    return jsonify(user_schema.dump(user))


@app.route("/logout")
@login_required
def logout():
    """
    Log the user out so session state is cleared.
    """
    logout_user()
    return jsonify({"messaged": "logged out"})


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """
    Register the user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        raise AlreadyExists(f"A user has already registered with {email}")

    new_user = User(id=uuid.uuid4(), email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))


app.register_blueprint(user_api)