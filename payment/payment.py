# flask server that renders the checkout.html file we created in the templates directory of the root folder.
import os

import stripe
from dotenv import load_dotenv  # this is to load the environment variables from the .env file!
from flask import Flask, render_template, request, redirect

load_dotenv()

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}

stripe.api_key = stripe_keys["secret_key"]


#############homepage where checkout button is shown#############
# this should be redirected from the UI when the "checkout/payment button is clicked first"
orderdata = None
@app.route('/payment', methods=['POST'])
def checkout():
    # data = request.get_json()
    data = request.get_data(as_text=True)
    print("data:", data)

    global orderdata
    orderdata = data

    # print(request)
    # total_price = data["total_price"]
    # customer_email = data["customer_email"]
    # customer_id = data["customer_id"]
    total_price = 10000
    customer_id = 1
    customer_email = "kwangkaixuan@gmail.com"
    # return render_template('checkout.html', key=stripe_keys['publishable_key'])  # this is the old one without passing data
    return render_template('checkout.html',key=stripe_keys['publishable_key'], total_price=total_price, customer_email=customer_email, customer_id=customer_id)

##################stripe checkout payment session for payment details############
@app.route('/charge', methods=['POST'])
def charge():
    # # check for total price sent by complex MS
    # data = request.get_json()
    # total_price = data["total_price"]

    amount = 1000  # Amount in cents #currently hardcoded

    customer = stripe.Customer.create(
        email='kwangkaixuan@gmail.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='sgd',
        description='Bluemart Purchase'
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
        # invalid payload
        # return "Invalid payload", 400 # this is the original one
        ### ignore the jsonify return first since it seems to be returning somewhere else
        # return jsonify(
        #     {
        #         "code": 400,
        #         "data": {},
        #         "message": "Payment Failed, Invalid Payload"
        #     }
        # )
        return render_template('chargefailed1.html', amount=amount)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        # return "Invalid signature", 400 #this is the original one
        ### ignore the jsonify return first since it seems to be returning somewhere else
        # return jsonify(
        #     {
        #         "code": 400,
        #         "data": {},
        #         "message": "Payment Failed, Invalid Signature"
        #     }
        # )
        return render_template('chargefailed2.html', amount=amount)

        # Handle the checkout.session.completed event

    ### the two lines below are from the other version of stripe's API, so "checkout.session.completed doesn't work" replace with charge.succeeded
    # if event["type"] == "checkout.session.completed":
    #     print("Payment was successful123")

    if event["type"] == "charge.succeeded":
        print("Payment Charge Confirmed")  # as long as this prints, the webhook is working properly.
        ### ignore the jsonify return first since it seems to be returning somewhere else
        # return jsonify(
        #     {
        #         "code": 200,
        #         "data": {},
        #         "message": "Payment Successful"
        #     }
        # )
        # let me try to redirect to payment complex MS here / redirect back to UI which will call checkout complex MS
        return redirect(f"/checkout")  # trying to redirect to complex #try if it works

    # return jsonify(
    #     {
    #         "code": 200,
    #         "data": {},
    #         "message": "Payment Successful"
    #     }
    # )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5069, debug=True)
