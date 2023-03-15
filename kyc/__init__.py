import markdown
import os
import sqlite3
import hashlib

from flask_cors import CORS
from flask import Flask, Response, request, json
from random import *

import kyc.database as db
import smtplib
import kyc.config as config
import sys

import nacl.signing
import nacl.encoding
import base64


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

signing_key = nacl.signing.SigningKey(config.HEX_SEED, encoder=nacl.encoding.HexEncoder)

conn = db.create_connection("/pythonsqlite.db")
db.create_db(conn)
db.run_migrations(conn)

app = Flask(__name__)
CORS(app, support_credentials=True, resources={r"*": {"origins": ["*"]}})

def send_email(to_email, message):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = config.SUBJECT
        msg['From'] = "tfconnect@incubaid.com"
        msg['To'] = to_email
        message = "<html><head></head><body><p>" + message + "</p></body></html>"
        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("tfconnect@incubaid.com", config.PASSWORD)

        server.sendmail("tfconnect@incubaid.com", to_email, msg.as_string())
        print('Mail has been sent.')
        server.quit()
    except Exception as woo:
        print(woo)

from kyc import routes