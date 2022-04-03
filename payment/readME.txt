- stripe.exe is the webhook command line app that must be run for the payment MS to track when a payment has been received successfully
- charge.html is a page template that is shown after user has made payment
- checkout.html is a page template that is shown for user to click on the button to make payment
- .env holds the API keys and webhook keys which will be retrieved from inside payment.py for authentication

Steps
1. Complex MS will do a redirection to @/payment to kickstart the payment process
2. Checkout.html will be rendered for user to make payment
3. After payment, charge.html will be rendered to show user that payment has been confirmed
4. User will can click on the button to go back to the homepage