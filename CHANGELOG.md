# Changelog

## v0.2.0

- **Breaking:** Anchor roles now use a functional controlled vocabulary, with descriptive part labels moved to `anchor.name`.
- Schema enforces non-empty `anchor.name` values and the new functional role set.
- Examples and narrative guidance updated to reflect functional roles.

Migration:

Before:
```yaml
anchors:
  - id: chair_seat
    owner_kind: object
    owner: chair
    name: seat
    role: seat
```

After:
```yaml
anchors:
  - id: chair_seat
    owner_kind: object
    owner: chair
    name: seat
    role: support_surface
```

## v0.1.0

- Initial specification draft with canonical schema, relations vocabulary, and narrative projection rules.
- Initial JSON Schema and example documents.
- Establishes two-layer model and conformance requirements.
