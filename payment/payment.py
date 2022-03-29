# flask server that renders the checkout.html file we created in the templates directory of the root folder.
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request, jsonify
import os
import stripe
from dotenv import load_dotenv #this is to load the environment variables from the .env file!
load_dotenv()

app = Flask(__name__)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}

stripe.api_key = stripe_keys["secret_key"]

#############homepage where checkout button is shown#############
@app.route('/')
def checkout():
    return render_template('checkout.html',key=stripe_keys['publishable_key'])

##################stripe checkout payment session for payment details############
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 1000

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='sgd',
        description='Flask Charge'
    )

    # redirects user to the payment success page
    return render_template('charge.html', amount=amount) 
###############webhook to confirm payment###############
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )
    except ValueError as e:
        #invalid payload
        # return "Invalid payload", 400 # this is the original one
        return jsonify(
            {
                "code": 400,
                "data": {},
                "message": "Payment Failed, Invalid Payload"
            }
        )
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        # return "Invalid signature", 400 #this is the original one
        return jsonify(
            {
                "code": 400,
                "data": {},
                "message": "Payment Failed, Invalid Signature"
            }
        )

    # Handle the checkout.session.completed event

    ### the two lines below are from the other version of stripe's API, so "checkout.session.completed doesn't work" replace with charge.succeeded
    # if event["type"] == "checkout.session.completed":
    #     print("Payment was successful123")

    if event["type"] == "charge.succeeded":
        print("Payment Charge Confirmed")
        return jsonify(
            {
                "code": 200,
                "data": {},
                "message": "Payment Successful"
            }
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5069, debug=True)