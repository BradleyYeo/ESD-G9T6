from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, cart_id, customer_id, product_id, product_name, price, quantity):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def json(self):
        return {"cart_id": self.cart_id, "customer_id": self.customer_id, "product_id": self.product_id,
                "product_name": self.product_name, "price": self.price, "quantity": self.quantity}