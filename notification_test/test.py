# #!/usr/bin/env python3
# # The above shebang (#!) operator tells Unix-like environments
# # to run this file as a python3 script

import json
import os

import pika
from flask import Flask, jsonify
from flask_cors import CORS

import amqp_setup

app = Flask(__name__)
CORS(app)


@app.route("/test", methods=['GET'])
def get_customer_cart():
    customer_id = 43
    customer_email = 'tianyu.chen.2020@smu.edu.sg'
    cart_items = [{
        "price": 256,
        "product_id": 1,
        "product_name": "apple",
        "quantity": 2
    },
        {
            "price": 256,
            "product_id": 2,
            "product_name": "banana",
            "quantity": 1
        }]
    try:
        publish_receipt(customer_id, customer_email, cart_items)
        return jsonify({"code": 200}), 200
    except:
        return jsonify({"code": 400}), 400


def publish_receipt(customer_id, customer_email, cart_items):
    amqp_setup.check_setup()
    order_id = 2
    total_price = 600
    message = {
        "created": "Wed, 16 Dec 2020 13:15:47 GMT",  # WIP
        "customer_id": customer_id,
        "customer_email": customer_email,
        "order_id": order_id,  # WIP
        "order_item": cart_items,
        "total_price": total_price  # WIP
    }
    print(str(message))
    message = json.dumps(message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#",
                                     body=message, properties=pika.BasicProperties(delivery_mode=2))


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=7000, debug=True)
