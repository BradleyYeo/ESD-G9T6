from flask import Flask, request, jsonify
from flask_cors import CORS

from os import environ

from models import InventoryModel, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


class NotEnoughStock(Exception):
    """Not enough stock"""
    pass


@app.route('/inventory/all')
def get_all():
    inventory = InventoryModel.query.all()
    if len(inventory):
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
            "data": {},
            "message": "There is no inventory recorded in the database"
        }
    )
    # return render_template('datalist.html', inventory=inventory)


@app.route('/inventory/', methods=['PUT'])
def update_inventory():
    data = request.get_json()
    product = InventoryModel.query.filter_by(product_id=data["product_id"]).first()
    try:
        new_quantity = int(data['quantity'])
        if product.quantity < new_quantity:
            raise NotEnoughStock
        else:
            product.quantity = new_quantity
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {},
                    "message": "Success"
                }
            ), 200

    except NotEnoughStock:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "items": [product]
                },
                "message": "Not enough stock"
            }
        )

        # return render_template('update.html', product=product)


if __name__ == "__main__":
    app.run("localhost", port=5552, debug=True)
