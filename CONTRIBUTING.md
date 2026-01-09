# Contributing

Thanks for helping improve the Pose Contact Specification! This repo is documentation- and schema-focused, so small, well-scoped changes are preferred.

## Workflow

1. **Choose the target file** in `spec/`, `schema/`, or `examples/`.
2. **Update or add content** with clear, concise language.
3. **Keep examples in sync** with any schema or spec edits.
4. **Validate everything**:

   ```bash
   python tools/validate_examples.py
   ```

5. **Update `CHANGELOG.md`** when you make a normative change to the specification or schema.

## Content guidance

- **Normative vs. informative:** Keep requirements in `spec/` clear and testable.
- **Terminology:** Reuse defined terms from `spec/terminology.md`.
- **Examples:** Prefer minimal examples that illustrate a single concept.

## File map

- `spec/`: Normative and informative specification documents.
- `schema/`: JSON Schema for canonical state validation.
- `examples/`: Example canonical/narrative files for validation.
- `tools/`: Validation helpers.
