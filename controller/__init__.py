"""
API setup
"""
from flask_principal import Principal

from controller.advice_controller import advice_api
from controller.user_controller import user_api
from core.application import app
from core.authentication import login_manager
import controller.identity_manager
import controller.error_handler

def init_app():
    principals = Principal(app)
    login_manager.init_app(app)
    app.register_blueprint(user_api)
    app.register_blueprint(advice_api)
