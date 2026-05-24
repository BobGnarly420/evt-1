# EVT-1

EVT-1 is a minimal, agent-first protocol for canonical product identity, trust assertions, provenance, and machine-readable verification.

## Protocol goals
- deterministic semantics
- inspectable trust
- agent interoperability
- low-friction deployment
- protocol-level extensibility

## Quick start (local, <15 minutes)
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python scripts/migrate.py
python scripts/seed.py
uvicorn app.main:app --reload
```
Open: http://127.0.0.1:8000/docs

## Docker
```bash
docker compose up --build
```

## API endpoints
- `GET /`
- `GET /health`
- `GET /resolve?q=`
- `GET /product/{product_id}`
- `POST /product`
- `POST /assert`
- `POST /verify`

## Architecture overview
- **Canonicalization engine** (`app/services/canonicalization.py`): deterministic normalization + aliasing + fuzzy matching via rapidfuzz.
- **Trust assertions** (`app/services/crypto.py` + API): Ed25519 signed claims with canonical JSON serialization.
- **Persistence** (`app/db`, `app/models`): SQLAlchemy + SQLite, product and assertion indexes.

## Threat model (MVP)
- Mitigates tampering through signatures and deterministic serialization.
- Preserves provenance and issuer attribution for independent trust signals.
- Does not solve identity binding to legal entities, key revocation infrastructure, or network-level adversaries.

## Trust model
Trust scores are probabilistic floats in `[0,1]` and can be independently asserted by multiple validators. The API preserves source, issuer, and signature verification metadata.

## Signing walkthrough
```python
from app.services.crypto import generate_keypair, sign_payload, verify_signature

sk, pk = generate_keypair()
payload = {"assertion_id": "a1", "issuer": "validator:demo", "subject": "urn:evt:product:sony-wh1000xm6-black", "claim": {"repairability": 0.81}, "timestamp": "2026-01-01T00:00:00Z"}
sig = sign_payload(sk, payload)
assert verify_signature(pk, payload, sig)
```

## Example assertions
See `app/data/sample_assertions.json`.

## Docs
- `docs/architecture.md`
- `docs/protocol.md`
- `docs/api.md`
- `docs/threat-model.md`

## License
Apache-2.0
