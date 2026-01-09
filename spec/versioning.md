# Versioning

This section is normative.

## Semantic Versioning

The specification uses semantic versioning (`MAJOR.MINOR.PATCH`).

- MAJOR increments indicate breaking changes to canonical schema or predicates.
- MINOR increments add backward-compatible predicates or optional fields.
- PATCH increments clarify text without changing validation behavior.
- Breaking changes MUST include a migration note and fixtures demonstrating old-to-new behavior.

## Backward Compatibility

- Canonical documents MUST declare `schema_version`.
- Implementations MUST reject documents with unknown MAJOR versions.
- Implementations SHOULD accept documents with equal MAJOR and higher MINOR versions when unknown fields are optional.
