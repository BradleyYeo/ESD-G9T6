from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InventoryModel(db.Model):
    __tablename__ = "table"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String())
    quantity = db.Column(db.Integer())
    price = db.Column(db.Integer())

    def __init__(self, id, product_name, quantity, price):
        self.product_id = id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"There are {self.quantity} {self.product_name} left"
