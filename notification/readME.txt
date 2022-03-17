Checkout (to do)
Queue (Done)
Notification (Done)
can design nicer looking email (KIV)


How to send the email:

0. change dir, open WAMP and docker desktop

0.1. from docker desktop, remove all rabbitMQ container (cos using same port as labs)

1. docker compose up

2. open rabbit mq ui http://localhost:15672/#/
username: guest
password: guest

3. in order_tracking exchange
click plublish a message
copy and paste the json from the api docs
https://docs.google.com/document/d/1jgMA_1-vBzY39Kcl245Ri2lU8B2eGpzNSs-NjXMgze0/edit

4. change the customer_email to an actual valid email account
if its invalid, there will be no error message, and email will not send
we will assume email will always be valid since user log in already

5. publish


############################################################
How to use google api/ what all the file does
############################################################

gmail account
username:
bluemart.business@gmail.com
password:
********************

credentials.json is from gmail OAuth google cloud 
create a new desktop user and download the credentials as json (rename it)

quickstart.py is from google api docs, 
this file uses credentials.json to create the token.json
will need to click allow in the popup browser
token.json is used as the 'api key'
(delete token.json) and reload this file if token gives error
https://developers.google.com/gmail/api/quickstart/python

send_email.py uses token.json to send an email
sender would be from bluemart.business@gmail.com since the gmail api is from this account
made with heavily modified code from google api docs,
https://developers.google.com/gmail/api/guides/sending

and some code from youtube guide:
https://youtube.com/watch?v=44ERDGa9Dr4
https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-in-python/

amqp_send_email.py uses amqp_send_email.py
consumes the json from rabbitMQ and use the data to send an email