from flask import jsonify, request, Blueprint
from flask_login import login_required

from api.exceptions import NotFound
from core.database import db
from model.stock import Stock, stock_schema, stocks_schema

stock_api = Blueprint('stock_api', __name__)


@stock_api.route("/stock", methods=["GET"])
@login_required
def get_stocks():
    all_stocks = Stock.query.all()
    return jsonify(stocks_schema.dump(all_stocks))


@stock_api.route("/stock", methods=["POST"])
@login_required
def create_stock():
    stock = Stock(ticker=request.json['ticker'])
    db.session.add(stock)
    db.session.commit()
    return jsonify(stock_schema.dump(stock))


@stock_api.route("/stock/<id>", methods=["GET"])
@login_required
def get_stock(id):
    stock = Stock.query.get(id)
    if (stock == None):
        raise NotFound(f"stock {id} not found")
    return jsonify(stock_schema.dump(stock))


@stock_api.route("/stock/<id>", methods=["DELETE"])
@login_required
def delete_stock(id):
    stock = Stock.query.get(id)
    if (stock == None):
        raise NotFound(f"stock {id} not found")
    db.session.delete(stock)
    db.session.commit()
    return jsonify(stock_schema.dump(stock))
