"""Minimal integration stub callable by agent tools."""
import requests

def resolve_product(query: str):
    return requests.get("http://127.0.0.1:8000/resolve", params={"q": query}, timeout=5).json()
