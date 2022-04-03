from os import environ

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class InventoryModel(db.Model):
    __tablename__ = "inventory"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String())
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, product_id, product_name, quantity, price):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def json(self):
        return {"product_id": self.product_id,
                "product_name": self.product_name,
                "quantity": self.quantity,
                "price": self.price}


# class NotEnoughStock(Exception):
#     """Not enough stock"""
#     pass


@app.route('/inventory/all')
def get_all():
    inventory = InventoryModel.query.all()
    if len(inventory):  # 1 and above is true in python
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [item.json() for item in inventory]
                },
                "message": "all items retrieved"
            }
        )
    return jsonify(
        {
            "code": 500,
            "message": "There is no inventory recorded in the database"
        }
    ), 500


@app.route('/inventory/reduce', methods=['PUT'])
def reduce_inventory():
    data = request.get_json()
    # check for existing item in inventory
    items = data["cart"]

    for item in items:
        product = InventoryModel.query.filter_by(product_id=item["product_id"]).first()
        if not product:
            return jsonify(
                {
                    "code": 404,
                    "data": {},
                    "message": "ItemID is invalid or does not exist."
                }
            ), 404

        new_quantity = int(item['quantity'])

        if new_quantity <= product.quantity:
            product.quantity -= new_quantity
            return jsonify(
                {
                    "code": 200,
                    "data": data,
                    "message": "Inventory decreased."
                }
            ), 200
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {},
                "message": "An error occurred when reducing items in inventory."
            }
        ), 500


@app.route("/inventory/add", methods=["PUT"])
def add_inventory():
    data = request.get_json()
    items = data["add"]
    for item in items:
        product = InventoryModel.query.filter_by(product_id=item["product_id"]).first()
        new_quantity = int(item['quantity'])
        product.quantity = new_quantity
        return jsonify(
            {
                "code": 200,
                "data": data,
                "message": "Inventory increased."
            }
        ), 200
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {},
                "message": "An error occurred when reducing items in inventory."
            }
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5552, debug=True)  # right number for docker compose
