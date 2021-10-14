import nacl
from kyc import signing_key


def sign(data):
    return signing_key.sign(data, encoder=nacl.encoding.Base64Encoder)