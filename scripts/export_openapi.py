"""Regenerate docs/openapi.json from the live app definition."""

import json
from pathlib import Path

from app.main import app

if __name__ == "__main__":
    out = Path("docs/openapi.json")
    out.write_text(json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n")
    print(f"wrote {out}")
