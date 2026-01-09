# Conformance

This section is normative.

## Canonical Conformance

An implementation conforms to this specification if it:

1. Produces and consumes canonical state documents that validate against the JSON Schema for structural and vocabulary validity.
2. Enforces reference integrity (all referenced identifiers exist) and invariant rules via higher-level validation tooling.
3. Rejects relations with invalid subject/object pairings or missing side disambiguation through higher-level validation.
4. Enforces anchor role membership in the functional vocabulary and requires anchor names to be non-empty descriptive strings.

## Narrative Projection Conformance

An implementation conforms to narrative projection requirements if it:

1. Generates projections exclusively from canonical state.
2. Ensures no projected statement contradicts or extends canonical facts.
3. Preserves identifiers and predicate semantics in projection text.

## Conformance Rule Enforcement Matrix

The table below maps each normative MUST requirement in the specification to its enforcement mechanism. Use JSON Schema for structural and controlled-vocabulary validation, and `tools/validate_examples.py` for higher-level semantic validation.

| Requirement (MUST) | Source | Enforcement |
| --- | --- | --- |
| Representation MUST be explicit, unambiguous, and machine-validated. | `spec/overview.md` (Problem Statement) | JSON Schema |
| Explicit facts MUST be preferred over inference. | `spec/overview.md` (Design Philosophy) | `tools/validate_examples.py` |
| The model MUST use minimal, orthogonal primitives. | `spec/overview.md` (Design Philosophy) | `tools/validate_examples.py` |
| The model MUST be independent of any engine or physics implementation. | `spec/overview.md` (Design Philosophy) | `tools/validate_examples.py` |
| Layer 1 (Canonical State) MUST be fully machine-validated. | `spec/overview.md` (Two-Layer Approach) | JSON Schema |
| Layer 2 (Narrative Projection) MUST NOT introduce or mutate facts. | `spec/overview.md` (Two-Layer Approach) | `tools/validate_examples.py` |
| The canonical layer MUST be sufficient to validate coherence without relying on narrative content. | `spec/overview.md` (Two-Layer Approach) | `tools/validate_examples.py` |
| The two-layer model MUST be used to ensure long-term coherence. | `spec/overview.md` (Rationale) | `tools/validate_examples.py` |
| Body parts that occur in left/right pairs MUST include a `side` attribute with `left` or `right`. | `spec/terminology.md` (Left/Right Disambiguation) | JSON Schema |
| Unpaired parts MUST use `none`. | `spec/terminology.md` (Left/Right Disambiguation) | `tools/validate_examples.py` |
| Implementations MUST NOT infer side from naming conventions. | `spec/terminology.md` (Left/Right Disambiguation) | `tools/validate_examples.py` |
| Actors MUST include `id`, `type`, and optional `label`. | `spec/data-model.md` (Actor) | JSON Schema |
| Actor `type` MUST be `human`. | `spec/data-model.md` (Actor) | JSON Schema |
| Body part references MUST include `kind` set to `body_part`. | `spec/data-model.md` (Body Part Reference) | JSON Schema |
| The controlled vocabulary for `part` MUST be enforced. | `spec/data-model.md` (Body Part Reference) | JSON Schema |
| Objects and surfaces MUST include `id` and optional `label`. | `spec/data-model.md` (Object and Surface) | JSON Schema |
| Anchors MUST include `id`, `owner_kind`, `owner`, `name`, and `role`. | `spec/data-model.md` (Anchor) | JSON Schema |
| `owner_kind` MUST be `object` or `surface`. | `spec/data-model.md` (Anchor) | JSON Schema |
| Anchor references MUST include `kind` set to `anchor`. | `spec/data-model.md` (Anchor) | JSON Schema |
| The controlled vocabulary for `role` MUST be enforced. | `spec/data-model.md` (Anchor) | JSON Schema |
| Each relation MUST include `id`, `predicate`, `subject`, and `object`. | `spec/data-model.md` (Relations) | JSON Schema |
| Implementations MUST enforce invariants via higher-level validation. | `spec/data-model.md` (Validation and Invariants) | `tools/validate_examples.py` |
| All referenced identifiers MUST exist. | `spec/data-model.md` (Validation and Invariants) | `tools/validate_examples.py` |
| All `predicate` values MUST be in the controlled vocabulary. | `spec/data-model.md` (Validation and Invariants) | JSON Schema |
| Body parts MUST include explicit side disambiguation. | `spec/data-model.md` (Validation and Invariants) | JSON Schema |
| Relations MUST NOT rely on narrative projections for validation. | `spec/data-model.md` (Validation and Invariants) | `tools/validate_examples.py` |
| Implementations MUST reject predicates outside the list. | `spec/relations.md` (Predicate Vocabulary) | JSON Schema |
| Relations MUST use subject/object pairings as specified. | `spec/relations.md` (Allowed Pairings) | `tools/validate_examples.py` |
| Qualifiers MUST NOT change predicate semantics. | `spec/relations.md` (Qualifiers) | `tools/validate_examples.py` |
| A narrative projection MUST be derived solely from canonical state. | `spec/narrative-projection.md` (Generation Rules) | `tools/validate_examples.py` |
| A narrative projection MUST NOT introduce new facts or modify canonical facts. | `spec/narrative-projection.md` (Generation Rules) | `tools/validate_examples.py` |
| A narrative projection MUST preserve predicate meanings and entity identities. | `spec/narrative-projection.md` (Generation Rules) | `tools/validate_examples.py` |
| A narrative projection MUST render the specific anchor `name` when describing anchors. | `spec/narrative-projection.md` (Generation Rules) | `tools/validate_examples.py` |
| Narrative projections MUST NOT be treated as authoritative. | `spec/narrative-projection.md` (Prohibitions) | `tools/validate_examples.py` |
| Narrative projections MUST NOT be used to validate canonical state. | `spec/narrative-projection.md` (Prohibitions) | `tools/validate_examples.py` |
| Narrative projections MUST NOT infer side, identity, or relation type when unspecified. | `spec/narrative-projection.md` (Prohibitions) | `tools/validate_examples.py` |
| Narrative projections MUST NOT create new anchors or change anchor ownership. | `spec/narrative-projection.md` (Prohibitions) | `tools/validate_examples.py` |
| Canonical documents MUST declare `schema_version`. | `spec/versioning.md` (Backward Compatibility) | JSON Schema |
| Implementations MUST reject documents with unknown MAJOR versions. | `spec/versioning.md` (Backward Compatibility) | `tools/validate_examples.py` |
