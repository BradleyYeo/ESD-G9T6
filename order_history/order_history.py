#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class Order_history(db.Model):
    __tablename__ = 'order_history'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    customer_id = db.Column(db.String(32), nullable=False)
    customer_email = db.Column(db.String(64), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'product_id': self.id, 'created': self.created, 'customer_id': self.customer_id,'customer_email': self.customer_email, 'order_id': self.order_id,'item_id': self.item_id, 'product_name': self.product_name, 'quantity': self.quantity, 'price': self.price, 'total_price': self.total_price}



@app.route("/order_history")
def get_all():
    orderlist = Order_history.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
   


@app.route("/order_history/<int:order_id>")
def find_by_order_id(order_id):
    orderlist = Order_history.query.filter_by(order_id=order_id)
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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
