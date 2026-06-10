# API

Interactive OpenAPI UI is served at `/docs` after boot.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Service name and status. |
| GET | `/health` | Liveness probe. |
| GET | `/resolve?q=` | Case-insensitive substring search over canonical product names. |
| GET | `/product/{product_id}` | Fetch a product by URN. `404` if unknown. |
| POST | `/product` | Create a product. The product URN is derived server-side via canonicalization. `409` if the URN already exists. |
| POST | `/assert` | Store a signed trust assertion. `400` on invalid signature, `409` on duplicate `assertion_id`. |
| POST | `/verify` | Verify an Ed25519 signature over a canonical-JSON payload. |

## Notes

- Product URNs follow `urn:evt:product:{manufacturer}-{model}-{variant}` (lowercased, non-alphanumerics collapsed to `-`).
- Signatures use Ed25519 over canonical JSON (sorted keys, compact separators); keys and signatures are base64-encoded.
- Trust scores are floats in `[0, 1]`.
