# Report

## Conclusions

- The canonical JSON Schema now uses only standard Draft 2020-12 features and loads cleanly in portable validators.
- Full conformance requires both schema validation for structure/vocabularies and higher-level validation tooling for reference integrity and predicate pairing rules.

## Validation Results

- Schema check (`validator_cls.check_schema`): PASS
- Canonical examples: PASS
- Invalid example failure reason: PASS (`anchors/0/role` rejects `seat` as intended)

### Tool Output

```text
Validation failed:
- invalid-example.yaml: anchors/0/role: 'seat' is not one of ['support_surface', 'contact_surface', 'rest_surface', 'handle', 'edge', 'corner', 'attachment_point']
```
