- stripe.exe is the webhook command line app that must be run for the payment MS to track when a payment has been received successfully. 
 - It is included here so that the webhook command can be typed in the same directory itself
- charge.html is a page template that is shown after user has made payment
- checkout.html is a page template that is shown for user to click on the button to make payment
- .env holds the API keys and webhook keys which will be retrieved from inside payment.py for authentication

Steps
0. While inside the payment folder directory, run the stripe webhook by typing stripe listen --forward-to 127.0.0.1:5069/webhook into a command window.
1. Click on the UI "Stripe checkout" button to do a redirection to @/payment to kickstart the payment process
2. Checkout.html will be rendered for user to make payment
3.1 After payment, charge.html will be rendered and shown to the user
3.2 Alongside the payment, the webhook listener should display the events when the Stripe API is called. In particular, look out for a print statement "Payment Confirmed" together with the event "Charge.succeeded" to verify payment. 
4.1 User will can click on the button to go back to the homepage
4.2 At this point, charge.html would have routed back to the Complex Microservice to continue on with the ordering process.