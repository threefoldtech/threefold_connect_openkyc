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

signing_key = nacl.signing.SigningKey(config.HEX_SEED, encoder=nacl.encoding.HexEncoder)

conn = db.create_connection("./pythonsqlite.db")
db.create_db(conn)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": ["*"]}})

def send_email(to_email, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(config.SUBJECT, msg)
        server.sendmail(config.EMAIL_ADDRESS, to_email, message)
        server.quit()
    except Exception as woo:
        print(woo)

from kyc import routes
