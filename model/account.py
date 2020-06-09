from core.database import db
from core.schemas import ma


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account

    id = ma.auto_field()
    email = ma.auto_field()


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
