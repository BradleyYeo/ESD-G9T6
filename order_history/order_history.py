#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script


from datetime import datetime
from os import environ

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'dbURL') or "mysql+mysqlconnector://is213@host.docker.internal:3306/order_history"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class OrderHistory(db.Model):
    __tablename__ = 'order_history'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    customer_email = db.Column(db.String(64), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_id, customer_email, order_id, total_price, item_id, product_name, quantity, price):
        self.customer_id = customer_id
        self.customer_email = customer_email
        self.order_id = order_id
        self.total_price = total_price
        self.item_id = item_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def json(self):
        return {'product_id': self.id, 'created': self.created, 'customer_id': self.customer_id,
                'customer_email': self.customer_email, 'order_id': self.order_id, 'item_id': self.item_id,
                'product_name': self.product_name, 'quantity': self.quantity, 'price': self.price,
                'total_price': self.total_price}


@app.route("/order_history")  # body MUST be None
def get_all():
    orderlist = OrderHistory.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )


@app.route("/order_history/<int:order_id>")  # body MUST be None
def find_by_order_id(order_id):
    orderlist = OrderHistory.query.filter_by(order_id=order_id)
    if orderlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404


@app.route("/order_history/add", methods=['POST'])
def add_order_to_order_history():
    data = request.get_json()

    # created = datetime.strptime(data["created"], '%d/%m/%y %H:%M:%S')
    customer_id = data["customer_id"]
    customer_email = data["customer_email"]
    order_id = data["order_id"]
    total_price = data["total_price"]

    order_item = data["order_item"]

    for item in order_item:
        item_id = item["product_id"]
        product_name = item["product_name"]
        quantity = item["quantity"]
        price = item["price"]
        order_row = OrderHistory(customer_id, customer_email,
                                 order_id, total_price, item_id, product_name, quantity, price)
        try:
            db.session.add(order_row)
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {},
                    "message": "An error occurred when creating new order row."
                }
            ), 500

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {},
                "message": "An error occurred when commiting new order."
            }
        ), 500

    return jsonify({
        "code": 200,
        "data": {},
        "message": "success"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
