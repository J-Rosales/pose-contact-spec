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
