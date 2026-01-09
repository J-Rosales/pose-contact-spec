# Data Model

This section is normative.

## Canonical Entities

The canonical state is a JSON/YAML document with the following top-level members:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema_version` | string | yes | Semantic version of the canonical schema. |
| `actors` | array | yes | List of actors (currently human actors only). |
| `objects` | array | no | List of environmental objects. |
| `surfaces` | array | no | List of environmental surfaces. |
| `relations` | array | yes | List of relations between entities. |

## Actor

Actors MUST include:

- `id` (string): Unique identifier within the document.
- `type` (string): MUST be `human`.
- `label` (string, optional): Human-readable label.

## Body Part Reference

Body parts are referenced within relations using:

- `kind`: MUST be `body_part`.
- `actor`: Actor `id`.
- `part`: Controlled vocabulary term.
- `side`: `left`, `right`, or `none`.

The controlled vocabulary for `part` is defined by the canonical schema and MUST be enforced. The initial vocabulary includes: `head`, `neck`, `torso`, `pelvis`, `shoulder`, `upper_arm`, `forearm`, `hand`, `thigh`, `calf`, `foot`.

## Object and Surface

Objects and surfaces MUST include:

- `id` (string): Unique identifier.
- `label` (string, optional): Human-readable label.

Objects and surfaces are referenced in relations using:

- `kind`: `object` or `surface`.
- `object` or `surface`: The referenced `id`.

## Relations

Each relation MUST include:

- `id` (string): Unique identifier.
- `predicate` (string): Controlled vocabulary value.
- `subject` (entity reference): The acting entity.
- `object` (entity reference): The target entity.

Optional `qualifiers` MAY be provided to disambiguate intensity or duration.

## Validation and Invariants

Implementations MUST enforce the following invariants:

1. All referenced `actor`, `object`, and `surface` identifiers MUST exist.
2. All `predicate` values MUST be in the controlled vocabulary.
3. Body parts MUST include explicit side disambiguation.
4. Relations MUST NOT rely on narrative projections for validation.
