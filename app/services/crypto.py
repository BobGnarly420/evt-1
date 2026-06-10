import base64
import json

from nacl.signing import SigningKey, VerifyKey


def canonical_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def generate_keypair() -> tuple[str, str]:
    sk = SigningKey.generate()
    pk = sk.verify_key
    return base64.b64encode(bytes(sk)).decode(), base64.b64encode(bytes(pk)).decode()


def sign_payload(private_key_b64: str, payload: dict) -> str:
    sk = SigningKey(base64.b64decode(private_key_b64))
    sig = sk.sign(canonical_json_bytes(payload)).signature
    return base64.b64encode(sig).decode()


def verify_signature(public_key_b64: str, payload: dict, signature_b64: str) -> bool:
    try:
        vk = VerifyKey(base64.b64decode(public_key_b64))
        vk.verify(canonical_json_bytes(payload), base64.b64decode(signature_b64))
        return True
    except Exception:
        return False
