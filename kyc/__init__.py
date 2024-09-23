
from flask_cors import CORS
from flask import Flask, Response, request, json
from random import *

import sendgrid
import kyc.database as db
from sendgrid.helpers.mail import Mail, Attachment
import kyc.config as config

import nacl.signing
import nacl.encoding


signing_key = nacl.signing.SigningKey(config.HEX_SEED, encoder=nacl.encoding.HexEncoder)

conn = db.create_connection("/pythonsqlite.db")
db.create_db(conn)
db.run_migrations(conn)

app = Flask(__name__)
CORS(app, support_credentials=True, resources={r"*": {"origins": ["*"]}})

def send_email(to_email, message):
    try:
        mail = Mail(from_email=config.EMAIL_ADDRESS, to_emails=[to_email], subject=config.SUBJECT, html_content=message)
        sg = sendgrid.SendGridAPIClient(config.PASSWORD)
        response = sg.client.mail.send.post(request_body=mail.get())
        print("Status code:", response.status_code)
        if response.status_code == 202:
            print('Mail has been sent.')
    except Exception as woo:
        print(woo)

from kyc import routes
