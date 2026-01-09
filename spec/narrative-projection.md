# Narrative Projection

This section is normative.

## Generation Rules

1. A narrative projection MUST be derived solely from the canonical state.
2. A narrative projection MUST NOT introduce new facts or modify canonical facts.
3. A narrative projection MAY omit canonical facts that are irrelevant to a given interaction.
4. A narrative projection MUST preserve predicate meanings and entity identities when described.
5. When describing anchors in Layer 2 text, a narrative projection MUST render the specific anchor `name` (e.g., "chair seat" vs. "top edge of chair back") as defined in the canonical state, and MAY include the functional `role` only as supporting context.

## Prohibitions

- Narrative projections MUST NOT be treated as authoritative.
- Narrative projections MUST NOT be used to validate canonical state.
- Narrative projections MUST NOT infer side, identity, or relation type when unspecified.
- Narrative projections MUST NOT create new anchors or change anchor ownership.

## Examples (Informative)

### Correct Projection

"The left hand of actor A is touching the right shoulder of actor B; actor A is standing on the floor."

### Incorrect Projection

"Actor A is supporting actor B" when the canonical relation is `touching` only.

## Guidance for LLM Usage (Informative)

- Provide only the subset of canonical facts necessary for the current turn.
- Include explicit identifiers and side disambiguation when referring to body parts.
- Avoid narrative embellishment that could be interpreted as new facts.
