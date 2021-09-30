import base64, requests, json, hashlib
import logging
import os

url = 'https://api.shuftipro.com/delete'

client_id = os.environ['SHUFTI_CLIENT_ID']
secret_key = os.environ['SHUFTI_SECRET_ID']


def get_shufti_data_by_reference(reference):
    url = 'https://api.shuftipro.com/status'

    status_request = {
        "reference": reference
    }

    # Calling Shufti Pro request API using python requests
    auth = '{}:{}'.format(client_id, secret_key)
    b64Val = base64.b64encode(auth.encode()).decode()
    # if access token
    # b64Val = access_token
    # replace "Basic with "Bearer" in case of Access Token
    response = requests.post(url,
                             headers={"Authorization": "Basic %s" % b64Val, "Content-Type": "application/json"},
                             data=json.dumps(status_request))

    # Calculating signature for verification
    # calculated signature functionality cannot be implement in case of access token
    calculated_signature = hashlib.sha256('{}{}'.format(response.content.decode(), secret_key).encode()).hexdigest()

    # Convert json string to json object
    json_response = json.loads(response.content)
    sp_signature = response.headers.get('Signature', '')

    if sp_signature == calculated_signature:
        return json_response

    print('Invalid Signature: {}'.format(json_response))


def delete_shufti_data_by_reference(reference):
    delete_request = {
        "reference": reference,
        "comment": "Automatic deletion of data"
    }

    # Calling Shufti Pro request API using python requests
    auth = '{}:{}'.format(client_id, secret_key)
    b64Val = base64.b64encode(auth.encode()).decode()

    response = requests.post(url,
                             headers={"Authorization": "Basic %s" % b64Val, "Content-Type": "application/json"},
                             data=json.dumps(delete_request))

    # Calculating signature for verification
    # calculated signature functionality cannot be implement in case of access token
    calculated_signature = hashlib.sha256('{}{}'.format(response.content.decode(), secret_key).encode()).hexdigest()

    # Convert json string to json object
    json_response = json.loads(response.content)
    sp_signature = response.headers.get('Signature', '')

    if sp_signature == calculated_signature:
        return json_response

    print('Invalid Signature: {}'.format(json_response))


def extract_data_from_callback(shufti_data):
    try:
        extracted_data = shufti_data['verification_data']['document']

        name = extracted_data['name']
        dob = extracted_data['dob']
        gender = extracted_data['gender']
        expiry_date = extracted_data['expiry_date']
        issue_date = extracted_data['issue_date']
        document_number = extracted_data['document_number']
        country = shufti_data['country']

        document_meta = {
            'expiry_date': expiry_date,
            'issue_date': issue_date,
            'document_number': document_number
        }

        data_object = {
            'name': name,
            'dob': dob,
            'gender': gender,
            'country': country,
            'document_meta': document_meta,
            'is_identified': 1
        }

        return data_object

    except Exception as e:
        logging.error('Could not parse the Shufti_data into JSON')
        logging.error(e)


def prepare_data_for_signing(data, user):
    country_data = bytes('{"identifier": "' + user[0] + '", "country_data": "'
                         + str(data['country']) + '"}', encoding='utf8')

    dob_data = bytes('{"identifier": "' + user[0] + '", "dob_data": "'
                     + str(data['dob']) + '"}', encoding='utf8')

    document_meta_data = bytes(
        '{"identifier": "' + user[0] + '", "document_meta_data": "' + str(data['document_meta']) + '"}',
        encoding='utf8')

    gender_data = bytes('{"identifier": "' + user[0] + '", "gender_data": "'
                        + str(data['gender']) + '"}', encoding='utf8')

    is_identified_data = bytes(
        '{"identifier": "' + user[0] + '", "is_identified_data": "' + str(data['is_identified']) + '"}',
        encoding='utf8')

    name_data = bytes('{"identifier": "' + user[0] + '", "name_data": "'
                      + str(data['name']) + '"}', encoding='utf8')

    return {
        'country_data': country_data,
        'dob_data': dob_data,
        'document_meta_data': document_meta_data,
        'gender_data': gender_data,
        'is_identified_data': is_identified_data,
        'name_data': name_data
    }
