import json
import os
from os import environ

from datetime import datetime

import pika
from flask import Flask, request, jsonify
from flask_cors import CORS

import amqp_setup
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

inventory_URL = environ.get('inventory_URL') or "http://inventory:5552/inventory"
cart_URL = environ.get('cart_URL') or "http://cart:5000/cart"


# payment_URL = environ.get('payment_URL') or "http://payment_placeholder:5553/payment"


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
        # except Exception as e:
    #     # Unexpected error in code
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     ex_str = str(e) + " at " + str(exc_type) + ": " + \
    #         fname + ": line " + str(exc_tb.tb_lineno)
    #     print(ex_str)
    #     return jsonify({
    #         "code": 500,
    #         "message": "place_order.py internal error: " + ex_str
    #     }), 500
    # if reached here, not a JSON request.
    # return jsonify({
    #     "code": 400,
    #     "message": "Invalid JSON input: " + str(request.get_data())
    # }), 400


def process_checkout(customer_id, customer_email):
    print("\n-----Invoking cart microservice-----")
    print("Getting customer's cart with their ID")
    cart_response = invoke_http(url=cart_URL + "/" + str(customer_id), method='GET', json=None)

    code = cart_response["code"]
    if code not in range(200, 300):
        print("Unexpected error from cart, exiting")
        return {"code": code, "message": str(cart_response)}

    print("Reterival of cart items success")
    cart_items = cart_response["data"]["cart"]

    print('\n-----Invoking inventory microservice-----')
    print("Removing qty from inventory with customer's cart")
    inventory_response = invoke_http(inventory_URL + "/reduce", method='PUT', json={"cart": cart_items})

    code = inventory_response["code"]
    print(str(inventory_response))
    ##################################################################################################
    if code not in range(200, 300):  # WIP
        print("Inventory returned error")
        if code == 500 and inventory_response["message"].lower() == "not enough stock.":
            print("Not enough stock in inventory")
            """To update the cart and user afterwards"""
            new_cart = inventory_response["data"]["cart"]
            print("invoke cart with new stock")
            # print(new_cart)
            ## TO DO
            #  cart_response = invoke_http(url=cart_URL + "/" + str(customer_id), method='PUT', json=max_stock)
            return {"code": code, "data": new_cart, "message": "Not enough stock."}
        else:
            print("Unexpected error from inventory, exiting")
            return {"code": code, "message": str(inventory_response)}
    ##################################################################################################

    elif inventory_response["message"].lower() == "inventory decreased.":
        print("Inventory check success")
    #     ##################################################################################################
    #     # print("\n-----Invoking payment microservice-----") #WIP
    #     # payment_method()
    #     ##################################################################################################
        print("\n-----Publishing receipt to message broker-----")
        publish_receipt(customer_id, customer_email, cart_items)

        print("\n-----Invoking cart microservice-----")
        print("Removing customer's cart with their ID")
        cart_response = invoke_http(url=cart_URL + "/remove_all/" + str(customer_id), method='PUT', json=None)

        code = cart_response["code"]
        if code not in range(200, 300):
            print("Unexpected error from cart, exiting")
            return {"code": code, "message": str(cart_response)}

        print("Everything is successful")
        return {"code": code, "message": "success"}


# def payment_method():
#     payment_response = invoke_http(url=payment_URL, method='POST', json=None)
#     if payment_response["code"] not in range(200, 300):
#         """unexpected error from payment"""
#         print("unexpected error from payment")
#     return {"code": payment_response["code"], "message": str(payment_response)}


def publish_receipt(customer_id, customer_email, cart_items):
    amqp_setup.check_setup()
    order_id = 2
    total_price = calcalate_total_price(cart_items)
    message = {
        "created": str(datetime.now()),
        "customer_id": customer_id,
        "customer_email": customer_email,
        "order_id": order_id,  ### WIP #append customer id and time stamp 
        "order_item": cart_items,
        "total_price": total_price
    }
    print(str(message))
    message = json.dumps(message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#",
                                     body=message, properties=pika.BasicProperties(delivery_mode=2))


def calcalate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item["price"]
    return total_price

#########################END###############################


    # message = json.dumps(order_result)
    # amqp_setup.check_setup()

    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as order fails-----')
    #     print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

    #     # invoke_http(error_URL, method="POST", json=order_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error",
    #                                      body=message, properties=pika.BasicProperties(delivery_mode=2))
    #     # make message persistent within the matching queues until it is received by some receiver
    #     # (the matching queues have to exist and be durable and bound to the exchange)

    #     # - reply from the invocation is not used;
    #     # continue even if this invocation fails
    #     print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), order_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"order_result": order_result},
    #         "message": "Order creation failure sent for error handling."
    #     }

    # # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # # In http version, we first invoked "Activity Log" and then checked for error.
    # # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched
    # # and a message sent to “Error” queue can be received by “Activity Log” too.

    # else:
    #     # 4. Record new order
    #     # record the activity log anyway
    #     #print('\n\n-----Invoking activity_log microservice-----')
    #     print(
    #         '\n\n-----Publishing the (order info) message with routing_key=order.info-----')

    #     # invoke_http(activity_log_URL, method="POST", json=order_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info",
    #                                      body=message)

    # print("\nOrder published to RabbitMQ Exchange.\n")
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails

    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')

    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result;
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as shipping fails-----')
    #     print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

    #     # invoke_http(error_URL, method="POST", json=shipping_result)
    #     message = json.dumps(shipping_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error",
    #                                      body=message, properties=pika.BasicProperties(delivery_mode=2))

    #     print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), shipping_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }

    # # 7. Return created order, shipping record
    # return {
    #     "code": 201,
    #     "data": {
    #         "order_result": order_result,
    #         "shipping_result": shipping_result
    #     }
    # }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for checkout MS...")
    app.run(host="0.0.0.0", port=5550, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
