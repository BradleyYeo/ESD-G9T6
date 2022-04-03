import os
import sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

order_history_URL = environ.get('order_history_URL') or "http://order_history:5001/order_history"

monitorBindingKey=''

def receiveOrderLog():
    amqp_setup.check_setup()
    queue_name = 'order_history'
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    message = json.loads(body)
    order_history_response = invoke_http(url=order_history_URL + "/add", method='POST', json=message)
    code = order_history_response["code"]
    if code not in range(200, 300):
        print("Unexpected error from order_history, exiting")
        print("code: " + code)
        print("message: " + order_history_response)



if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
