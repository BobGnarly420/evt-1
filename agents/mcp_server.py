"""MCP server exposing EVT-1 to any MCP-compatible agent (Claude Code, Claude Desktop, etc.).

Run against a live EVT-1 API (default http://127.0.0.1:8000, override with EVT1_BASE_URL):

    python agents/mcp_server.py

Or register in an MCP client config:

    {"mcpServers": {"evt1": {"command": "python", "args": ["agents/mcp_server.py"]}}}
"""

import os

import httpx
from mcp.server.fastmcp import FastMCP

from app.services.crypto import generate_keypair as _generate_keypair
from app.services.crypto import sign_payload, verify_signature

BASE_URL = os.getenv("EVT1_BASE_URL", "http://127.0.0.1:8000")

mcp = FastMCP("evt1")


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10)


@mcp.tool()
def resolve_product(query: str) -> list[dict]:
    """Resolve a free-text product name to canonical EVT-1 product URNs.

    Returns a list of {product_id, canonical_name} matches.
    """
    with _client() as c:
        r = c.get("/resolve", params={"q": query})
        r.raise_for_status()
        return r.json()


@mcp.tool()
def get_trust_profile(product_id: str) -> dict:
    """Fetch a product's full trust profile by canonical URN.

    Includes trust scores (identity_confidence, counterfeit_risk, vendor_reliability,
    repairability, claim_verifiability, return_friction), provenance, and signatures.
    """
    with _client() as c:
        r = c.get(f"/product/{product_id}")
        r.raise_for_status()
        return r.json()


@mcp.tool()
def submit_assertion(
    assertion_id: str,
    issuer: str,
    subject: str,
    claim: dict,
    timestamp: str,
    signature: str,
    public_key: str,
    provenance: dict | None = None,
) -> dict:
    """Submit a signed trust assertion about a product.

    The signature must be Ed25519 over the canonical JSON of
    {assertion_id, issuer, subject, claim, timestamp} (sorted keys, compact separators).
    Rejected with 400 if the signature is invalid, 409 if assertion_id already exists.
    """
    body = {
        "assertion_id": assertion_id,
        "issuer": issuer,
        "subject": subject,
        "claim": claim,
        "timestamp": timestamp,
        "signature": signature,
        "public_key": public_key,
        "provenance": provenance or {},
    }
    with _client() as c:
        r = c.post("/assert", json=body)
        r.raise_for_status()
        return r.json()


@mcp.tool()
def verify_assertion(payload: dict, signature: str, public_key: str) -> dict:
    """Verify an Ed25519 signature over a canonical-JSON payload, without storing anything.

    Verification happens locally; no network round trip or trust in the server is required.
    """
    return {"valid": verify_signature(public_key, payload, signature)}


@mcp.tool()
def generate_keypair() -> dict:
    """Generate a new Ed25519 keypair (base64-encoded) for issuing trust assertions.

    Keep the private key secret; publish the public key alongside your assertions.
    """
    sk, pk = _generate_keypair()
    return {"private_key": sk, "public_key": pk}


@mcp.tool()
def sign_assertion(
    private_key: str,
    assertion_id: str,
    issuer: str,
    subject: str,
    claim: dict,
    timestamp: str,
) -> dict:
    """Sign a trust assertion payload with an Ed25519 private key.

    Returns the signature plus the exact payload that was signed, ready for submit_assertion.
    """
    payload = {
        "assertion_id": assertion_id,
        "issuer": issuer,
        "subject": subject,
        "claim": claim,
        "timestamp": timestamp,
    }
    return {"payload": payload, "signature": sign_payload(private_key, payload)}


if __name__ == "__main__":
    mcp.run()
