import os
import random

from flask import Flask, jsonify

from api.exceptions import AlreadyExists, Unauthorized, NotFound
from api.stock_api import stock_api
from api.user_api import user_api
from core.authentication import login_manager
from core.database import db
from core.schemas import ma

app = Flask("WSBBOT")
app.config.from_object(os.getenv('APP_SETTINGS', 'core.config.DevelopmentConfig'))
db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)


@app.errorhandler(Exception)
def handle_unknown(error):
    app.logger.error(error)
    response = jsonify({"message": "unknown error"})
    response.status_code = 500
    return response


@app.errorhandler(NotFound)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Unauthorized)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(AlreadyExists)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/", methods=["GET"])
def index():
    terms = [
        "Stonks only go up",
        "Pump and dump",
        "All Time High",
        "Due Diligence",
        "It's different this time",
        "Don't fight the fed"
    ]
    return terms[random.randrange(0, len(terms))]


app.register_blueprint(user_api)
app.register_blueprint(stock_api)
