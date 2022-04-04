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