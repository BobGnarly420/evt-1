"""Minimal integration stub callable by agent tools."""

import httpx


def resolve_product(query: str):
    return httpx.get("http://127.0.0.1:8000/resolve", params={"q": query}, timeout=5).json()
