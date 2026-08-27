# EVT-1

[![CI](https://github.com/BobGnarly420/evt-1/actions/workflows/ci.yml/badge.svg)](https://github.com/BobGnarly420/evt-1/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)

**TLS certificates, but for product claims.** EVT-1 is a minimal, agent-first
protocol that gives AI agents a shared way to agree on *what a product is*
(deterministic canonical URNs) and to verify *claims about it* (Ed25519-signed
trust assertions) — without trusting the marketplace that displayed them.

```bash
# Resolve a messy listing to a canonical identity...
curl "http://127.0.0.1:8000/resolve?q=sony+wh-1000xm6"
# [{"product_id": "urn:evt:product:sony-wh1000xm6-black", "canonical_name": "Sony WH-1000XM6"}]

# ...then pull its trust profile: counterfeit risk, repairability, vendor reliability,
# plus independently signed assertions any agent can verify locally.
curl "http://127.0.0.1:8000/product/urn:evt:product:sony-wh1000xm6-black"
```

## Why

Shopping and procurement agents currently inherit whatever a marketplace tells
them. Different sellers describe the same product differently, and trust
signals (reviews, badges, "verified" labels) are unverifiable platform
artifacts. EVT-1 fixes both at the protocol level:

- **Canonical identity** — `urn:evt:product:{manufacturer}-{model}-{variant}`,
  derived deterministically (normalization + alias resolution + fuzzy match
  confidence). Two agents canonicalizing the same product get the same URN.
- **Inspectable trust** — anyone can sign a claim (`{"repairability": 0.81}`)
  over canonical JSON with an Ed25519 key. Agents verify signatures
  themselves; the server stores and serves, it is not a trust root.

## Use it from an agent (MCP)

EVT-1 ships an [MCP](https://modelcontextprotocol.io) server so any
MCP-compatible agent (Claude Code, Claude Desktop, ...) gets the full
workflow as tools: `resolve_product`, `get_trust_profile`, `generate_keypair`,
`sign_assertion`, `submit_assertion`, `verify_assertion`.

```bash
pip install -e .[mcp]
python agents/mcp_server.py          # talks to EVT1_BASE_URL (default localhost:8000)
```

Client config (see `examples/mcp_config.json`):

```json
{"mcpServers": {"evt1": {"command": "python", "args": ["agents/mcp_server.py"]}}}
```

LLM-readable protocol summary: [`llms.txt`](llms.txt). Machine-readable API
schema: [`docs/openapi.json`](docs/openapi.json).

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

| Method | Path | Description |
|---|---|---|
| GET | `/resolve?q=` | Fuzzy-resolve free text to canonical product URNs |
| GET | `/product/{product_id}` | Full trust profile for a product |
| POST | `/product` | Register a product (URN derived server-side) |
| POST | `/assert` | Store a signed trust assertion (signature checked) |
| POST | `/verify` | Verify a signature over a canonical-JSON payload |
| GET | `/health`, `/` | Liveness / service info |

Full details: [`docs/api.md`](docs/api.md).

## Architecture overview

- **Canonicalization engine** (`app/services/canonicalization.py`):
  deterministic normalization + aliasing + fuzzy matching via rapidfuzz.
- **Trust assertions** (`app/services/crypto.py` + API): Ed25519 signed
  claims with canonical JSON serialization (sorted keys, compact separators).
- **Persistence** (`app/db`, `app/models`): SQLAlchemy + SQLite, product and
  assertion indexes.
- **MCP server** (`agents/mcp_server.py`): the protocol as agent tools.

## Threat model (MVP)

- Mitigates tampering through signatures and deterministic serialization.
- Preserves provenance and issuer attribution for independent trust signals.
- Does not solve identity binding to legal entities, key revocation
  infrastructure, or network-level adversaries. See
  [`docs/threat-model.md`](docs/threat-model.md).

## Trust model

Trust scores are probabilistic floats in `[0,1]` and can be independently
asserted by multiple validators. The API preserves source, issuer, and
signature verification metadata.

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

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/protocol.md`](docs/protocol.md)
- [`docs/api.md`](docs/api.md)
- [`docs/threat-model.md`](docs/threat-model.md)
- [`docs/openapi.json`](docs/openapi.json)
- [`llms.txt`](llms.txt)

## License

Apache-2.0
