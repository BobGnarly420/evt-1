import anyio
import pytest

pytest.importorskip("mcp")


def test_mcp_server_registers_all_tools():
    from agents.mcp_server import mcp

    tools = {t.name for t in anyio.run(mcp.list_tools)}
    assert tools == {
        "resolve_product",
        "get_trust_profile",
        "submit_assertion",
        "verify_assertion",
        "generate_keypair",
        "sign_assertion",
    }


def test_local_tools_sign_and_verify_without_server():
    from agents.mcp_server import generate_keypair, sign_assertion, verify_assertion

    keys = generate_keypair()
    signed = sign_assertion(
        private_key=keys["private_key"],
        assertion_id="mcp-unit-1",
        issuer="validator:unit",
        subject="urn:evt:product:sony-wh1000xm6-black",
        claim={"repairability": 0.81},
        timestamp="2026-06-10T00:00:00Z",
    )
    assert verify_assertion(signed["payload"], signed["signature"], keys["public_key"]) == {
        "valid": True
    }
    assert (
        verify_assertion(signed["payload"], signed["signature"], generate_keypair()["public_key"])
        == {"valid": False}
    )
