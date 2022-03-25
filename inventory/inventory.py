from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:root@localhost:8889/inventory"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
CORS(app)


class InventoryModel(db.Model):
    __tablename__ = "inventory"

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


class NotEnoughStock(Exception):
    """Not enough stock"""
    pass


@app.route('/inventory/all')
def get_all():
    inventory = InventoryModel.query.all()
    if len(inventory): # 1 and above is true in python
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
    # return render_template('datalist.html', inventory=inventory)


# @app.route('/inventory/', methods=['PUT'])
# def update_inventory():
#     data = request.get_json()
#     product = InventoryModel.query.filter_by(product_id=data["product_id"]).first()
#     try:
#         new_quantity = int(data['quantity'])
#         if product.quantity < new_quantity:
#             raise NotEnoughStock
#         else:
#             product.quantity = new_quantity
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": {},
#                     "message": "Success"
#                 }
#             ), 200
#
#     except NotEnoughStock:
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "items": [product]
#                 },
#                 "message": "Not enough stock"
#             }
#         )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5552, debug=True)
