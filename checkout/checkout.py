# #!/usr/bin/env python3
# # The above shebang (#!) operator tells Unix-like environments
# # to run this file as a python3 script
import json
import os
import time
from datetime import datetime
from os import environ

import pika
from flask import Flask, request, jsonify
from flask_cors import CORS

import amqp_setup
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

inventory_URL = environ.get('inventory_URL') or "http://inventory:5552/inventory"
cart_URL = environ.get('cart_URL') or "http://cart:5000/cart"


@app.route("/checkout", methods=['POST'])
def checkout():
    try:
        user_info = request.get_json()
        customer_email = user_info["customer_email"]
        customer_id = user_info["customer_id"]
        print("\nReceived a checkout request with customer_id: ", customer_id)

        result = process_checkout(customer_id, customer_email)
        print('\n------------------------')
        print('\nresult: ', result)
        return jsonify(result), result["code"]

    except:
        return


@app.route("/checkout/payment_success", methods=['POST'])
def checkout_payment_success():
    try:
        user_info = request.get_json()
        customer_email = user_info["customer_email"]
        customer_id = user_info["customer_id"]
        print("\nReceived a checkout request with customer_id: ", customer_id)
        result = process_checkout_payment_success(customer_id, customer_email)
        print('\n------------------------')
        print('\nresult: ', result)
        return jsonify(result), result["code"]

    except:
        return


def process_checkout(customer_id, customer_email):
    print("\n-----Invoking cart microservice-----")
    print("Getting customer's cart with their ID")
    cart_response = invoke_http(url=cart_URL + "/" + str(customer_id), method='GET', json=None)

    code = cart_response["code"]
    if code not in range(200, 300):
        if code == 404 and cart_response["message"].lower() == "cart is empty.":
            return {"code": code, "message": "Cart is empty."}
        else:
            print("Unexpected error from cart, exiting")
            return {"code": code, "message": str(cart_response)}

    print("Retrieval of cart items success")
    cart_items = cart_response["data"]["cart"]

    print('\n-----Invoking inventory microservice-----')
    print("Removing qty from inventory with customer's cart")
    inventory_response = invoke_http(inventory_URL + "/reduce", method='PUT', json={"cart": cart_items})

    code = inventory_response["code"]
    print(str(inventory_response))

    if code not in range(200, 300):
        print("Inventory returned error")
        if code == 500 and inventory_response["message"].lower() == "not enough stock.":
            print("Not enough stock in inventory")
            """To update the cart and user afterwards"""
            new_cart = inventory_response["data"]["cart"]

            print("invoke cart with new stock")
            cart_response = invoke_http(url=cart_URL + "/update/" + str(customer_id), method='PUT', json=new_cart)
            if cart_response["code"] == 200 and cart_response["message"].lower() == "cart updated.":
                return {"code": code, "data": new_cart, "message": "Not enough stock, cart updated to max stock"}
            else:
                return {"code": code, "data": new_cart,
                        "message": "Not enough stock, cart unexpectedly failed to update to max stock"}
        else:
            print("Unexpected error from inventory, exiting")
            return {"code": code, "message": str(inventory_response)}


    elif inventory_response["message"].lower() == "inventory decreased.":
        print("Inventory check success")
        return {
            "code": code,
            "data": {
                "customer_id": customer_id,
                "cart": cart_items
            },
            "message": "Inventory check success, inventory decreased"
        }

    # ##################################################################################################
    # Invoking payment microservice done with UI
    # ##################################################################################################


def process_checkout_payment_success(customer_id, customer_email):
    print("\n-----Invoking cart microservice-----")
    print("Getting customer's cart with their ID")
    cart_response = invoke_http(url=cart_URL + "/" + str(customer_id), method='GET', json=None)

    code = cart_response["code"]
    if code not in range(200, 300):
        if code == 404 and cart_response["message"].lower() == "cart is empty.":
            return {"code": code, "message": "Cart is empty."}  # should never happen
        else:
            print("Unexpected error from cart, exiting")
            return {"code": code, "message": str(cart_response)}

    print("Retrieval of cart items success")
    cart_items = cart_response["data"]["cart"]

    print("\n-----Publishing receipt to message broker-----")
    publish_receipt(customer_id, customer_email, cart_items)

    print("\n-----Invoking cart microservice-----")
    print("Removing customer's cart with their ID")
    cart_response = invoke_http(url=cart_URL + "/remove_all/" + str(customer_id), method='PUT', json=None)

    code = cart_response["code"]
    if code not in range(200, 300):
        print("Unexpected error from cart, exiting")
        return {"code": code, "message": str(cart_response)}
    print("Everything is successful.")
    return {"code": code, "message": "Everything is successful."}


def publish_receipt(customer_id, customer_email, cart_items):
    amqp_setup.check_setup()
    order_id = get_order_id()  # every sec is a new unique order_id
    total_price = calculate_total_price(cart_items)
    message = {
        "created": str(datetime.now()),
        "customer_id": customer_id,
        "customer_email": customer_email,
        "order_id": order_id,
        "order_item": cart_items,
        "total_price": total_price
    }
    print(str(message))
    message = json.dumps(message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#",
                                     body=message, properties=pika.BasicProperties(delivery_mode=2))


def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item["price"]
    return total_price


def get_order_id():
    date_time_str = '03/04/22 00:00:00'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    unix_timestamp = time.mktime(date_time_obj.timetuple())
    now_unix_timestamp = time.mktime(datetime.now().timetuple())
    return int(now_unix_timestamp - unix_timestamp)


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for checkout MS...")
    app.run(host="0.0.0.0", port=5550, debug=True)
