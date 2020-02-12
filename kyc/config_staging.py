import os

EMAIL_ADDRESS = "info@openkyc.live"
HEX_SEED = os.environ['SEED']
PASSWORD =  os.environ['PASSWORD']
SUBJECT = "Verify your email address"
REDIRECT_URL = "http://192.168.1.184:8081/verifyemail"
