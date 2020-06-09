from flask import jsonify, request, Blueprint

from core.database import db
from api.exceptions import NotFound
from model.account import Account, account_schema, accounts_schema

account_api = Blueprint('account_api', __name__)

@account_api.route("/account", methods=["GET"])
def get_accounts():
    all_accounts = Account.query.all()
    return jsonify(accounts_schema.dump(all_accounts))


@account_api.route("/account", methods=["POST"])
def create_account():
    account = Account(email=request.json['email'])
    db.session.add(account)
    db.session.commit()
    return jsonify(account_schema.dump(account))


@account_api.route("/account/<id>", methods=["GET"])
def get_account(id):
    account = Account.query.get(id)
    if (account == None):
        raise NotFound(f"account {id} not found")
    return jsonify(account_schema.dump(account))


@account_api.route("/account/<id>", methods=["DELETE"])
def delete_account(id):
    account = Account.query.get(id)
    if (account == None):
        raise NotFound(f"account {id} not found")
    db.session.delete(account)
    db.session.commit()
    return jsonify(account_schema.dump(account))
