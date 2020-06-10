import os
import random
import logging

from flask import Flask, jsonify

from core.database import db
from core.schemas import ma
from api.exceptions import BaseException

from api.account_api import account_api
from api.stock_api import stock_api

app = Flask("WSBBOT")
app.config.from_object(os.getenv('APP_SETTINGS', 'core.config.DevelopmentConfig'))
db.init_app(app)
ma.init_app(app)

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(error)
    response = jsonify({'message': "unknown error"})
    response.status_code = 500
    return response


@app.errorhandler(BaseException)
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
    return jsonify(terms[random.randrange(0, len(terms))])

app.register_blueprint(account_api)
app.register_blueprint(stock_api)