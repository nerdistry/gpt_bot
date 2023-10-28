"""
A utility script to set up sending a WhatsApp message through the Twilio Messaging API.
"""

# Standard library import
import logging

# Third-party imports
from twilio.rest import Client
from decouple import config


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text=None, media_url=None):
    try:
        if media_url:
            message = client.messages.create(
                from_=f"whatsapp:{twilio_number}",
                media_url=[media_url],
                to=f"whatsapp:{to_number}"
            )
            print("Twilio Response:", message)
            logger.info(f"Media message sent to {to_number}: {message.sid}")
        elif body_text:
            message = client.messages.create(
                from_=f"whatsapp:{twilio_number}",
                body=body_text,
                to=f"whatsapp:{to_number}"
            )
            logger.info(f"Text message sent to {to_number}: {message.body}")
        else:
            logger.warning("No text or media URL provided for message.")
            return

    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")