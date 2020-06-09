from core.database import db
from core.schemas import ma


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))


class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stock

    id = ma.auto_field()
    ticker = ma.auto_field()


stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
