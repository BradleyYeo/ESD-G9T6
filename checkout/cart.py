# #!/usr/bin/env python3
# # The above shebang (#!) operator tells Unix-like environments
# # to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/cart/<string:customer_id>", methods=['GET'])
def get_customer_cart(customer_id):
    return_value = {
        "code": 200,
        "data": {
            "customer_id": customer_id,
            "cart_items": [
                {
                    "product_id": 1,
                    "product_name": "apple",
                    "quantity": 2,
                    "price": 256
                }, {
                    "product_id": 2,
                    "product_name": "banana",
                    "quantity": 1,
                    "price": 256
                }
            ]
        },
        "message": "items retrieved for customer with product_id found in data"
    }
    return jsonify(return_value), 200


@app.route("/cart/remove_all/<string:customer_id>", methods=['PUT'])
def remove_customer_cart(customer_id):
    result = {
        "code": 200,
        "data": {},
        "message": "Success"
    }
    return jsonify(result), 200


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
