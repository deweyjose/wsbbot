import random

from flask import Blueprint

from core.application import app

advice_api = Blueprint('advice_api', __name__)

solid_advice = [
        "Stonks only go up",
        "Pump and dump",
        "All Time High",
        "Due Diligence",
        "It's different this time",
        "Don't fight the fed",
        "Buy low sell high",
        "Buy high sell high"
    ]

@app.route("/advice", methods=["GET"])
def index():
    """
    The root route. Returns a random popular WSB phrase.
    """

    return solid_advice[random.randrange(0, len(solid_advice))]
