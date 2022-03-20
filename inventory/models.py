from os import environ

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from inventory.inventory import app

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
CORS(app)

class InventoryModel(db.Model):
    __tablename__ = "table"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String())
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, id, product_name, quantity, price):
        self.product_id = id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def json(self):
        return {"product_id": self.product_id,
                "product_name": self.product_name,
                "quantity": self.quantity,
                "price": self.price}
