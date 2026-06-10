import re

from rapidfuzz import fuzz

ALIASES = {
    "sony corp": "sony",
    "sony corporation": "sony",
    "apple inc": "apple",
}

def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def canonicalize(manufacturer: str, model: str, variant: str) -> tuple[str, float, dict]:
    mf_raw = manufacturer.strip().lower()
    mf = ALIASES.get(mf_raw, mf_raw)
    confidence = fuzz.ratio(mf_raw, mf) / 100.0
    pid = f"urn:evt:product:{norm(mf)}-{norm(model)}-{norm(variant)}"
    explain = {
        "manufacturer_input": manufacturer,
        "manufacturer_canonical": mf,
        "match_confidence": confidence,
    }
    return pid, max(confidence, 0.75), explain
