# AGENTS instructions for EVT-1

## Architectural principles
- Keep protocol semantics deterministic and inspectable.
- Prefer explicit, typed models over dynamic behavior.
- Preserve provenance and signatures as first-class fields.

## Coding conventions
- Python 3.12, type hints required on public functions.
- Pydantic v2 for API schemas.
- SQLAlchemy ORM for persistence.
- Keep modules small and composable.

## Protocol invariants
- Product IDs use `urn:evt:product:{manufacturer}-{model}-{variant}`.
- Canonical JSON for signing uses sorted keys and compact separators.
- Trust scores are floats in `[0,1]`.

## Constraints
- No cloud dependencies.
- No message queue, no distributed orchestration.
- No frontend app in this repo.

## Non-goals
- Enterprise IAM/Authz.
- Vendor-specific dashboards.
- Non-deterministic ranking logic.

## Extension strategy
- Add optional fields without breaking required contract.
- Add new trust claims via assertion payloads.
- Add storage backends behind same repository interfaces only when needed.
