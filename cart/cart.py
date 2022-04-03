from os import environ

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


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


# GET ALL CART IN DB
@app.route("/cart")
def get_all():
    cartlist = Cart.query.all()
    if len(cartlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "carts": [cart.json() for cart in cartlist]
                },
                "message": "Cart items retrieved."
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": "There are no items"
        }
    ), 400


# GET CART OF ONE CUSTOMER
@app.route("/cart/<int:customer_id>")
def get_cart(customer_id):
    cartlist = Cart.query.filter_by(customer_id=customer_id).all()
    if cartlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "cart": [cart.json() for cart in cartlist]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "data": {},
            "message": "There is no item in cart."
        }
    ), 400


# ADD ITEM TO CART
@app.route("/cart/add", methods=['POST'])
def add_to_cart():
    cart_id = 0
    data = request.get_json()
    cart = Cart(cart_id=cart_id, customer_id=data['customer_id'], product_id=data['product_id'],
                product_name=data['product_name'], price=data['price'], quantity=data['quantity'])
    # if item is already in cart

    try:
        db.session.add(cart)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {},
                "message": "Item added to cart."
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {},
                "message": "An error occured creating the cart"
            }
        ), 500


# REMOVE ALL ITEMS FROM CUSTOMER'S CART
@app.route("/cart/remove_all/<int:customer_id>", methods=['PUT'])
def remove_all(customer_id):
    # if cart is empty
    cart = Cart.query.filter_by(customer_id=customer_id).all()
    if not cart:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "customer_id": customer_id
                },
                "message": "Cart is empty."
            }
        ), 404

    # else remove all items in cart
    try:
        for item in cart:
            db.session.delete(item)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {},
                "message": "Cart is removed."
            }
        ), 200
    except:
        return jsonify(
            {
                "code": 500,
                "data": {},
                "message": "An error occurred while removing all cart items… Can’t connect to MySQL server on ‘localhost:3306’"
            }
        ), 500


# UPDATE QUANTITY OF ONE ITEM IN CUSTOMER'S CART
@app.route("/cart/update", methods=["PUT"])
def update_cart():
    data = request.get_json()
    # check for existing item in cart
    item = Cart.query.filter_by(customer_id=data['customer_id'], product_id=data['product_id']).first()
    if not item:
        return jsonify(
            {
                "code": 404,
                "data": {},
                "message": "Item not in cart."
            }
        ), 404

    try:
        new_quantity = int(data['quantity'])
        item.quantity = new_quantity
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": data,
                "message": "Cart updated."
            }
        ), 200
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "quantity": data
                },
                "message": "An error occurred while updating the cart items… Can’t connect to MySQL server on ‘localhost:3306’"
            }
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
