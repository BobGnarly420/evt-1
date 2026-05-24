from app.services.crypto import canonical_json_bytes, generate_keypair, sign_payload, verify_signature

def test_signature_roundtrip():
    sk, pk = generate_keypair()
    payload = {"b": 2, "a": 1}
    sig = sign_payload(sk, payload)
    assert verify_signature(pk, payload, sig)

def test_canonical_json_deterministic():
    assert canonical_json_bytes({"b":2,"a":1}) == b'{"a":1,"b":2}'
