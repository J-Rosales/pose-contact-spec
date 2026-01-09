# Roadmap

This document lists deferred items and their acceptance criteria.

## Deferred items

- Publish a machine-readable canonical schema.
  - Acceptance criteria:
    - `schema/` includes a versioned JSON Schema artifact.
    - `SPEC_INDEX.md` links to the published schema file.

- Expand conformance tests for edge cases.
  - Acceptance criteria:
    - `tests/` includes fixtures for invalid inputs that cover each predicate.
    - CI runs the conformance suite in a single command.

- Provide a reference validator CLI.
  - Acceptance criteria:
    - `src/` ships a CLI that validates a document and exits non-zero on failure.
    - Documentation in `README.md` shows example usage with expected output.
