# Specification Index

Use this reading order for a linear, first-time pass through the spec. Each document links to the next conceptual layer.

## Recommended reading order

1. **Overview** — goals, scope, and non-goals.
   - `spec/overview.md`
2. **Terminology** — canonical definitions and shared vocabulary.
   - `spec/terminology.md`
3. **Data model** — entities, fields, and required structure.
   - `spec/data-model.md`
4. **Relations** — how entities connect (contact, support, constraints).
   - `spec/relations.md`
5. **Narrative projection** — Layer 2 rules and projection guidance.
   - `spec/narrative-projection.md`
6. **Conformance** — validation expectations and implementation guidance.
   - `spec/conformance.md`
7. **Versioning** — evolution rules for the specification.
   - `spec/versioning.md`

## Contributor workflow (short form)

1. Make your change in `spec/`, `schema/`, or `examples/`.
2. Keep examples aligned with the spec and schema.
3. Validate everything:

   ```bash
   python tools/validate_examples.py
   ```

4. Update `CHANGELOG.md` for normative spec or schema changes.
