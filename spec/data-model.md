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
| `anchors` | array | no | List of anchors that belong to objects or surfaces. |
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

## Anchor

Anchors are optional, locally named regions that belong to exactly one object or surface.

Anchors MUST include:

- `id` (string): Unique identifier within the document.
- `owner_kind` (string): MUST be `object` or `surface`.
- `owner` (string): The referenced object or surface `id`.
- `name` (string): Locally meaningful descriptive name within the owning object or surface.
- `role` (string): Controlled vocabulary functional role.

Anchor `name` values SHOULD use a consistent, lowercase, delimiter-based convention (e.g., `snake_case`) to preserve local meaning without expanding the functional role vocabulary.

Anchors are referenced in relations using:

- `kind`: MUST be `anchor`.
- `anchor`: The referenced anchor `id`.

The controlled vocabulary for `role` is defined by the canonical schema and MUST be enforced. The initial vocabulary includes: `support_surface`, `contact_surface`, `rest_surface`, `handle`, `edge`, `corner`, `attachment_point`.

## Relations

Each relation MUST include:

- `id` (string): Unique identifier.
- `predicate` (string): Controlled vocabulary value.
- `subject` (entity reference): The acting entity.
- `object` (entity reference): The target entity.

Optional `qualifiers` MAY be provided to disambiguate intensity or duration.

## Validation and Invariants

Implementations MUST enforce the following invariants:

1. All referenced `actor`, `object`, `surface`, and `anchor` identifiers MUST exist.
2. All `predicate` values MUST be in the controlled vocabulary.
3. Body parts MUST include explicit side disambiguation.
4. Relations MUST NOT rely on narrative projections for validation.
