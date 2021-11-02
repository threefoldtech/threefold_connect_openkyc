import os

EMAIL_ADDRESS = "info@openkyc.live"
HEX_SEED = os.environ['SEED']
PASSWORD =  os.environ['PASSWORD']
SUBJECT = "Verify your email address"
REDIRECT_URL = os.environ['URL']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']