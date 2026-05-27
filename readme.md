# Grid KYC OpenKYC

Grid KYC OpenKYC is a Python Flask service that provides email and phone verification with cryptographically signed attestations. It enables downstream services to trust verified contact information without storing sensitive personal data.

## What this is

Grid KYC OpenKYC exposes RESTful endpoints for verifying user contact information. Users register with a user ID and email address or phone number, receive a verification code, and upon successful verification receive a cryptographically signed attestation. The service uses ed25519 signatures to produce tamper-proof attestations that other services can validate independently.

The service also integrates with Shufti Pro for advanced identity verification (KYC) workflows.

## What this repository contains

- `kyc/` — Flask application with route handlers, database models, and configuration
- `helpers/` — Cryptographic signing utilities and Shufti Pro integration helpers
- `openkyc.py` — Application entry point
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container build definition
- `helm_files/` — Kubernetes deployment manifests

## Role in the stack

Grid KYC OpenKYC functions as an identity verification microservice. It can be deployed alongside authentication services, user management systems, or any infrastructure that requires verified contact information. The signed attestations it produces can be consumed by other services without those services needing direct access to personal data.

## Relation to ThreeFold

This technology is used within the ThreeFold ecosystem and was first deployed on the ThreeFold Grid. The component itself is designed as reusable infrastructure technology and should be understood by its technical function first, independent of any specific deployment.

## Ownership

This repository is owned and maintained by TF-Tech NV, a Belgian company responsible for the development and maintenance of this technology.

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

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.
