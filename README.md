# ESD-G9T6
# Instructions to run Bluemart web app
Open docker desktop
Start WAMP server
Ensure the whole folder is in WAMP/MAMP directory (./www/)

Load inventory.sql from inventory package into phpMyAdmin
Load cart.sql from cart package into phpMyAdmin
Load order_history.sql from order_history package into phpMyAdmin

Ensure rabbit mq is not running as we are using the same port as the labs

Run docker-compose up

In a new command window inside the payment folder, run the stripe webhook to listen for user payments  by typing stripe listen --forward-to 127.0.0.1:5069/webhook (your device must be registered and authorized inside Stripe API as a local listener for this to work)