# Pose Contact Spec Confidence Report

## 1) Executive status (1 page max)

**Current spec version:** v0.2.0 (latest entry in CHANGELOG; examples target `schema_version: 0.2.0`).【F:CHANGELOG.md†L3-L34】【F:examples/canonical-minimal.yaml†L1-L29】

**What changed since last version (from CHANGELOG):**
- **Breaking:** Anchor roles moved to a functional controlled vocabulary, with descriptive labels moved to `anchor.name`.【F:CHANGELOG.md†L3-L28】
- Schema now enforces non-empty `anchor.name` values and the new functional role set; examples and narrative guidance updated accordingly.【F:CHANGELOG.md†L5-L29】

**Breaking or non-breaking:** Breaking (anchor role vocabulary change) per CHANGELOG.【F:CHANGELOG.md†L3-L7】

**Are we on track?**
- **Mostly, but blocked by schema validation:** The spec and schema align on top-level fields, controlled vocabularies, and anchor semantics (PASS checks below), but JSON Schema validation currently fails because the schema uses `$data` enums that the reference validator rejects; this prevents automated example validation from running successfully.【F:schema/pose-contact.schema.json†L68-L203】
- **Spec rules not fully enforceable in schema:** The spec requires reference integrity and subject/object pairing rules, but the schema does not encode these constraints (or uses non-standard `$data`), so conformance enforcement is incomplete at the schema layer.【F:spec/data-model.md†L81-L88】【F:spec/relations.md†L26-L34】【F:schema/pose-contact.schema.json†L90-L203】

## 2) Spec ↔ Schema alignment checklist

| Check | Status | Evidence (spec ↔ schema) |
| --- | --- | --- |
| Canonical top-level fields: `schema_version`, `actors`, `objects`, `surfaces`, `anchors`, `relations` | **PASS** | Spec table lists all fields; schema properties match and require `schema_version`, `actors`, `relations`.【F:spec/data-model.md†L5-L16】【F:schema/pose-contact.schema.json†L5-L33】 |
| Entity kinds supported by `entity_ref` (including `anchor`) | **PASS** | Spec defines body_part/object/surface/anchor references; schema `entity_ref` includes those four kinds.【F:spec/data-model.md†L26-L68】【F:schema/pose-contact.schema.json†L105-L164】 |
| Controlled vocabularies: predicates | **PASS** | Spec predicate list matches schema enum list.【F:spec/relations.md†L5-L24】【F:schema/pose-contact.schema.json†L175-L199】 |
| Controlled vocabularies: `body_part` terms | **PASS** | Spec lists body-part vocabulary; schema enum matches.【F:spec/data-model.md†L26-L35】【F:schema/pose-contact.schema.json†L105-L129】 |
| Controlled vocabularies: `anchor.role` functional vocabulary | **PASS** | Spec role vocabulary list matches schema enum list.【F:spec/data-model.md†L49-L68】【F:schema/pose-contact.schema.json†L68-L88】 |
| Conformance rules enforceable by schema vs informative | **PARTIAL** | Schema enforces required fields, enums, and anchor name non-empty; spec also requires reference integrity and subject/object pairing rules that are **not** expressed in the schema (and `$data` usage is not accepted by the validator).【F:spec/data-model.md†L81-L88】【F:spec/relations.md†L26-L34】【F:spec/conformance.md†L5-L13】【F:schema/pose-contact.schema.json†L68-L203】 |

## 3) Example validation results

**Validation status:** `python tools/validate_examples.py` fails during schema validation because `$data` enums are not accepted by the JSON Schema validator (see Appendix for verbatim output). This prevents automated example validation from executing.

| Example file | Status | Notes (static reasoning due to validation failure) |
| --- | --- | --- |
| `examples/canonical-minimal.yaml` | NOT EXECUTED | Should pass: uses required top-level fields, valid predicates, body parts, and surface refs.【F:examples/canonical-minimal.yaml†L1-L29】【F:schema/pose-contact.schema.json†L7-L203】 |
| `examples/canonical-chair-anchors.yaml` | NOT EXECUTED | Should pass: anchor roles are in functional vocabulary and anchor names are non-empty; relations target anchors as allowed by spec.【F:examples/canonical-chair-anchors.yaml†L1-L40】【F:spec/relations.md†L26-L34】【F:schema/pose-contact.schema.json†L68-L203】 |
| `examples/canonical-human-human.yaml` | NOT EXECUTED | Should pass: body part refs and predicates are valid; surfaces referenced by ID.【F:examples/canonical-human-human.yaml†L1-L44】【F:schema/pose-contact.schema.json†L105-L203】 |
| `examples/canonical-human-object.yaml` | NOT EXECUTED | Should pass: valid `gripping` predicate and object/surface refs; schema supports object/surface entity refs.【F:examples/canonical-human-object.yaml†L1-L30】【F:schema/pose-contact.schema.json†L131-L203】 |
| `examples/invalid-example.yaml` | NOT EXECUTED | Should fail **for intended reason**: `anchor.role: seat` is not in the functional role enum (`support_surface`, `contact_surface`, etc.).【F:examples/invalid-example.yaml†L1-L24】【F:schema/pose-contact.schema.json†L68-L88】 |
| `examples/narrative-projection.txt` | N/A | Non-canonical narrative text; not validated against schema. It is explicitly non-authoritative. 【F:examples/narrative-projection.txt†L1-L6】【F:spec/narrative-projection.md†L13-L18】 |

## 4) Two-layer integrity check

- **Layer 1 is authoritative:** The overview explicitly states Layer 1 (Canonical State) is authoritative and must be machine-validated.【F:spec/overview.md†L20-L24】
- **Narrative projection is non-authoritative:** Narrative Projection section prohibits treating projections as authoritative and forbids introducing new facts.【F:spec/narrative-projection.md†L7-L18】
- **No place where Layer 2 can introduce canonical facts:** Narrative Projection rules require derivation solely from canonical state and prohibit introducing/modifying facts or creating anchors, ensuring Layer 2 cannot add canonical facts.【F:spec/narrative-projection.md†L7-L18】

## 5) Anchor semantics sanity check

- **`anchor.role` is functional and small/stable:** Functional role vocabulary is defined in the spec and enforced by schema (support/contact/rest surfaces, handle, edge, corner, attachment point).【F:spec/data-model.md†L53-L68】【F:schema/pose-contact.schema.json†L77-L88】
- **`anchor.name` is descriptive and local:** Spec requires a locally meaningful descriptive name and recommends lowercase conventions; schema enforces non-empty strings.【F:spec/data-model.md†L55-L61】【F:schema/pose-contact.schema.json†L75-L77】
- **Chair “seat vs back_top” expressed via name, not role:** Example anchors use `name: seat` vs `name: back_top` while sharing the same functional role (`support_surface`).【F:examples/canonical-chair-anchors.yaml†L9-L19】
- **Relation pairings include anchor where appropriate, and exclude nonsensical pairings:** Spec explicitly allows anchors in relevant predicate pairings (e.g., `sitting_on`, `supporting`) and defines allowed pairings to prevent invalid combinations; schema does not enforce pairings but spec-level rule is clear.【F:spec/relations.md†L26-L34】【F:schema/pose-contact.schema.json†L175-L203】

## 6) Known gaps / deferred items

1) **Schema uses `$data` enums that are rejected by the validator.**
   - **Impact:** Validation tooling cannot run; example validation currently fails before evaluating any instance files.
   - **Recommended next action:** **Schema change** to replace `$data` with JSON Schema-compliant mechanisms (or switch tooling to a validator that supports `$data`).【F:schema/pose-contact.schema.json†L90-L156】

2) **Reference integrity rules are required by spec but not reliably enforced by schema.**
   - **Impact:** Spec demands that referenced IDs exist; schema does not enforce this (the `$data` approach is non-standard).
   - **Recommended next action:** **Schema change** or **validator extension** to enforce reference existence, plus test coverage in tools/validation pipeline.【F:spec/data-model.md†L81-L86】【F:schema/pose-contact.schema.json†L90-L156】

3) **Subject/object pairing rules are specified but not enforced in schema.**
   - **Impact:** Implementations relying solely on schema could accept nonsensical pairings that the spec forbids.
   - **Recommended next action:** **Schema change** (e.g., conditional subschemas per predicate) or **validation script enhancement** to enforce pairing rules beyond schema validation.【F:spec/relations.md†L26-L34】【F:spec/conformance.md†L9-L13】

4) **No explicit binding of `schema_version` to a concrete version in schema.**
   - **Impact:** Schema validates any semantic version pattern, even when spec version is known and current examples target `0.2.0`.
   - **Recommended next action:** **Schema change** or tooling enforcement to ensure allowed major/minor versions match the published spec version policy.【F:schema/pose-contact.schema.json†L9-L12】【F:examples/canonical-minimal.yaml†L1-L29】【F:spec/versioning.md†L5-L17】

---

## Appendix: Validation output (verbatim)

```
Traceback (most recent call last):
  File "/workspace/pose-contact-spec/tools/validate_examples.py", line 64, in <module>
    sys.exit(main())
             ^^^^^^
  File "/workspace/pose-contact-spec/tools/validate_examples.py", line 51, in main
    errors = validate_examples(schema, examples_dir)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/pose-contact-spec/tools/validate_examples.py", line 27, in validate_examples
    validator_cls.check_schema(schema)
  File "/root/.pyenv/versions/3.12.12/lib/python3.12/site-packages/jsonschema/validators.py", line 316, in check_schema
    raise exceptions.SchemaError.create_from(error)
jsonschema.exceptions.SchemaError: {'$data': '/objects/*/id'} is not of type 'array'

Failed validating 'type' in metaschema['properties']['definitions']['additionalProperties']['$dynamicRef']['allOf'][1]['properties']['allOf']['items']['$dynamicRef']['allOf'][1]['properties']['then']['$dynamicRef']['allOf'][1]['properties']['properties']['additionalProperties']['$dynamicRef']['allOf'][3]['properties']['enum']:
    {'type': 'array', 'items': True}

On schema['definitions']['anchor']['allOf'][0]['then']['properties']['owner']['enum']:
    {'$data': '/objects/*/id'}
```
