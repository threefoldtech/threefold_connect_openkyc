# ThreeFold Connect OpenKYC

OpenKYC is a Python Flask service for the ThreeFold Connect ecosystem that provides email and phone verification for user identities. It allows users to register with a user ID and email address or phone number, receive a verification code, and upon verification returns a cryptographically signed attestation of the verified contact information.

## Overview

The service exposes RESTful endpoints for:

- **Email verification**: Sending verification emails and confirming email addresses
- **Phone/SMS verification**: Sending verification SMS messages and confirming phone numbers
- **KYC integration**: Integration with Shufti Pro for identity verification workflows

Verified data is signed using ed25519 cryptographic signatures, enabling downstream services to trust the attestation without storing sensitive personal data.

## Structure

- `kyc/` – Flask application with route handlers, database models, and configuration
- `helpers/` – Cryptographic signing utilities and Shufti Pro integration helpers
- `openkyc.py` – Application entry point

## Development

Setup:
```bash
python3 -m venv py_env
pip install -r requirements.txt
```

Run:
```bash
export FLASK_APP=openkyc.py
flask run --reload --debugger -p 5005 --host 0.0.0.0
```

## Deploy

```bash
export PASSWORD=<insert password>
gunicorn -b localhost:5005 -w 1 kyc:app
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
Copyright (c) TFTech NV.
