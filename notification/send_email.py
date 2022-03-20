# with refrence from : gmail api docs
# https: // developers.google.com/gmail/api

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def decompose_input_to_email(json_data):
    """
    using json input to push into
    create_message(to, subject, message_text)
    message text in HTML is created here

        Args:
    json_data: raw json data received from the que, 
                see api documentations for example data

    Returns:
        An object containing a base64url encoded email object.
    """

    order_id = json_data['order_id']
    order_item = json_data['order_item']
    total_price = f'{int(json_data["total_price"])/100:.2f}'

    to = json_data['customer_email']
    subject = f"Order receipt from Bluemart. Order ID: {order_id}"

    message_text = ""
    message_text += '<h1 style="color:blue;">BlueMart</h1>'
    message_text += '<table border=1>'
    message_text += '<tr><th> Items </th><th> Quantity </th></tr>'
    for item in order_item:
        message_text += f"<tr><td>{item['product_name']}</td><td>{item['quantity']}</td></tr>"
    message_text += '</table>'
    message_text += f'<h3>The total price is ${total_price}</h3>'
    message_text += '<h3>Thank you for your purchace!</h3>'
    message_text += '<p style="color:grey;font-style:italic">this is a system generated email, please do not reply to it</p>'
    return create_message(to, subject, message_text)


def create_message(to, subject, message_text):
    """
    Create a message for an email.

    Args:
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, _subtype='HTML')
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(email_object):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            service = build('gmail', 'v1', credentials=creds)
        else:
            print("credentials not found")
    except:
        print("credentials failed to load")

    user_id='me'
    try:
        message = (service.users().messages().send(userId=user_id, body=email_object).execute())
        print('Message Id: %s' % message['product_id'])
        return message
    except:
        print('Email failed to send')