# Overview

## Problem Statement (Normative)

A representation of articulated human pose and body-part contact MUST be explicit, unambiguous, and machine-validated. Informal prose and model-internal state are insufficient for long-lived correctness because they drift, omit invariants, and cannot be reliably diffed or validated. This specification defines a canonical, declarative state model and a non-authoritative narrative projection.

## Intended Use Cases (Informative)

- Instruction and planning for embodied agents.
- Analysis and annotation of observed interactions.
- Choreography and staging descriptions.
- Reasoning and validation of contact and support constraints.

## Design Philosophy (Normative)

- Explicit facts MUST be preferred over inference.
- The model MUST use minimal, orthogonal primitives.
- The model MUST be independent of any engine or physics implementation.

## Two-Layer Approach (Normative)

- Layer 1 (Canonical State) is the authoritative source of truth and MUST be fully machine-validated.
- Layer 2 (Narrative Projection) is a derived, selective representation for communication to a language model and MUST NOT introduce or mutate facts.
- The canonical layer MUST be sufficient to validate coherence without relying on narrative content.

## Rationale (Normative)

Language models do not maintain stable internal state or preserve invariants across long histories. Prose-only representations drift, and symbol-only representations lose meaning without context. The two-layer model MUST therefore be used to ensure long-term coherence while enabling reliable reasoning and instruction.
