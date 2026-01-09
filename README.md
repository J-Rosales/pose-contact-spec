# Pose Contact Specification

This repository defines a formal, declarative specification for representing articulated human pose, body-part contact, support, and interaction with the environment. The specification is designed to be unambiguous, machine-parseable, human-authorable, and suitable for validation and long-term versioning.

## Two-Layer Schema Model (Normative)

The specification defines a mandatory two-layer schema model:

1. **Canonical State (Layer 1):** The authoritative, lossless, machine-validated representation of facts, relations, constraints, and history. Layer 1 is the sole source of truth.
2. **Narrative Projection (Layer 2):** A selective, natural-language-oriented projection derived from the canonical state to communicate relevant information to a language model at a given turn. Layer 2 MUST NOT introduce new facts or contradict Layer 1.

Coherence and correctness are guaranteed only by the canonical layer. Narrative projections are informative and non-authoritative.

## Non-Goals

The specification does not:

- Encode animation curves or motion trajectories.
- Encode forces or physics simulation.
- Depend on any rendering, animation, or physics engine.
- Depend on natural-language inference to establish truth.

## Repository Structure

- `spec/`: Normative and informative specification documents.
- `schema/`: JSON Schema for canonical state validation.
- `examples/`: Canonical and narrative projection examples.
- `CHANGELOG.md`: Version history.

