from kyc import app, signing_key, nacl, db, conn, send_email
from flask_cors import CORS
from flask import Flask, Response, request, json
from datetime import datetime, timedelta
from random import *
import os
import string
import markdown
import kyc.config as config
import time
import base64
import hashlib
import logging


logging.getLogger("werkzeug").setLevel(level=logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)s()]: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

logger.addHandler(handler)

@app.route("/verification/send-email", methods=['POST'])
def verify_email_handler():
    body = request.get_json()
    logger.debug('body %s', body)

    user_id = body.get('user_id').lower()
    email = body.get('email')
    redirect_url = config.REDIRECT_URL + "/verifyemail"
    public_key = body.get('public_key')
    resend = body.get('resend')
    letters = string.ascii_uppercase + string.ascii_lowercase + string.ascii_letters
    verification_code = ''.join(choice(letters) for i in range(randint(64, 128)))
    user = db.getUserByName(conn, user_id)

    logger.debug("verification_code: %s", verification_code)

    union = "?"

    if union in redirect_url:
        union = "&"

    url = "{}{}userId={}&verificationCode={}".format(redirect_url, union, user_id, verification_code)
    logger.debug("url: %s", url)

    html = "Hi {} <br><br> You have just created a Threefold Connect account.<br> On behalf of the Threefold Connect team, we hereby provide a link to verify your email address. When you click on this link, you will be taken to a page confirming your address is verified.<br> Without this verification, not all features will be available.<br> <a href=""{}>Verify my email address</a><br><br> Thanks,<br>OpenKYC Team".format(user_id, url)
    
    try:
        if not user:
            logger.debug("not user")
            db.insert_user(conn, user_id, email, verification_code, 0, public_key, "")
        else:
            logger.debug("updating using verficiation code, because we already have an entry.")
            db.update_user_verification_code(conn, user_id, verification_code)

        logger.debug("Sending email...")
        send_email(email, html)
        
        return Response("Mail sent")
    except Exception as exception:
        logger.debug("Exception")
        return Response("Something went wrong", status=500)

@app.route("/verification/verify-email", methods=['POST'])
def verify_handler():
    body = request.get_json()
    userid = body.get('user_id').lower()
    verification_code = body.get('verification_code')
    user = db.getUserByName(conn, userid)

    if user:
        if verification_code == user[2]:
            data = bytes('{ "email": "' + user[1] + '", "identifier": "' + user[0] + '" }', encoding='utf8')
            signed_email_identifier = signing_key.sign(data, encoder=nacl.encoding.Base64Encoder)
        
            if signed_email_identifier: 
                db.update_user(conn, "UPDATE users SET signed_email_identifier = ? WHERE user_id = ?", signed_email_identifier.decode("utf-8"), user[0])
                logger.debug("Successfully verified userid %s", user[0])
                return signed_email_identifier
            else:
                return Response('Something went wrong.', status=403)
        else:
            logger.debug("Attempted to verify userid %s with an incorrect verification_code %s", userid, verification_code)
            return Response('Something went wrong.', status=403)
    else:
        logger.debug("No open verifications found for userid %s", userid)
        return Response('Something went wrong.', status=403)

@app.route("/verification/retrieve-sei/<userid>", methods=['GET'])
def get_signed_email_identifier_handler(userid):
    userid = userid.lower()
    user = db.getUserByName(conn, userid)

    if user is None:
        logger.debug("User was not found.")
        return Response("User was not found.", status=404)

    signed_data_verification_response = verify_signed_data(user[0], request.headers.get('Jimber-Authorization'), user[4], "get-signedemailidentifier")

    if(isinstance(signed_data_verification_response, Response)):
        logger.debug("response of verification is of instance Response, failed to verify.")
        return signed_data_verification_response

    if len(user) >= 5 and not user[5]:
        logger.debug("We found an old account: %s", user[0])

        if user[3] == 1:
            logger.debug("Old account was verified, creating signature.")
            
            data = bytes('{ "email": "' + user[1] + '", "identifier": "' + user[0] + '" }', encoding='utf8')
            signed_email_identifier = signing_key.sign(data, encoder=nacl.encoding.Base64Encoder)

            sei = {"signed_email_identifier": signed_email_identifier.decode("utf-8")}

            response = app.response_class(
                response=json.dumps(sei),
                mimetype='application/json'
            )
            
            logger.debug("SEI: %s", sei)
            return response

        else:
            logger.debug("Old account was not verified. User needs to resend the email.")
            return Response("something went wrong", status=404)

    if user[5]:
        logger.debug("We found an account: %s", user[0])
        logger.debug("Retrieved signed_email_identifier for %s", userid)

        db.delete_user(conn, user[0], user[1])

        data = {"signed_email_identifier": user[5]}

        logger.debug("data: %s", data)

        response = app.response_class(
            response=json.dumps(data),
            mimetype='application/json'
        )

        return response
    else:
        return Response("User not found in database.", status=404)

@app.route("/verification/public-key", methods=['GET'])
def public_key_handler():
    data = {"public_key": signing_key.verify_key.encode(encoder=nacl.encoding.Base64Encoder).decode("utf8")}

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response

@app.route("/verification/verify-sei", methods=['POST'])
def verification_handler():
    try:
        body = request.get_json()
        public_key = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)

        verify_key = nacl.signing.VerifyKey(public_key, encoder=nacl.encoding.HexEncoder)

        sei_decoded = base64.b64decode(body.get("signedEmailIdentifier"))
        sei = verify_key.verify(sei_decoded)

        logger.debug("Successfully verified signature: %s", sei.decode('utf-8'))

        response = app.response_class(
            response = sei,
            mimetype = 'application/json'
        )

        return response
    except Exception as exception:
        logger.debug("Invalid or corrupted signature for sid: %s", body.get("signedEmailIdentifier"))
        return Response("Invalid or corrupted signature", status=500)

def verify_signed_data(double_name, data, encoded_public_key, intention, expires_in = 3600):
    if data is not None:
        decoded_data = base64.b64decode(data)

        bytes_data = bytes(decoded_data)

        public_key = base64.b64decode(encoded_public_key)
        verify_key = nacl.signing.VerifyKey(public_key.hex(), encoder=nacl.encoding.HexEncoder)

        verified_signed_data = verify_key.verify(bytes_data)

        if verified_signed_data:
            verified_signed_data = json.loads(verified_signed_data.decode("utf-8"))
            if(verified_signed_data["intention"] == intention):
                timestamp = verified_signed_data["timestamp"]
                readable_signed_timestamp = datetime.fromtimestamp(int(timestamp) / 1000)
                current_timestamp = time.time() * 1000
                readable_current_timestamp = datetime.fromtimestamp(int(current_timestamp / 1000))
                difference = (int(timestamp) - int(current_timestamp)) / 1000
                # All negative times are accepted, we should refactor this to take the timeout into account and the possibility that the users time is a bit wrong.
                if difference <= expires_in:
                    logger.debug("Jimber-Authorization-Header verified.")
                    return verified_signed_data
                else:
                    logger.debug("Timestamp was expired took %s instead of %s", difference, expires_in)
                    return Response("something went wrong", status=404)
            else:
                logger.debug("Wrong intention.")
                return Response("something went wrong", status=404)
        else:
            logger.debug("Jimber-Authorization-Header could not be verified.")
            return Response("something went wrong", status=404)
    else:
        logger.debug("No data to sign.")
        return Response("something went wrong", status=404)
