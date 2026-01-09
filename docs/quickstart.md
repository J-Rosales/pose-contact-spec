# Quickstart

This quickstart introduces the two-layer model, shows a canonical YAML example with its narrative projection, and outlines the minimal author workflow for creating valid pose-contact data.

## Two-layer model at a glance

The specification is a mandatory two-layer schema model:

- **Layer 1: Canonical state (authoritative).** A lossless, machine-validated record of facts, relations, constraints, and history. This is the sole source of truth.
- **Layer 2: Narrative projection (non-authoritative).** A selective, natural-language projection derived from the canonical state for a specific interaction. It must not add facts or contradict Layer 1.

Narrative text is informative only; correctness is guaranteed solely by the canonical layer.

## Canonical YAML example (Layer 1)

```yaml
schema_version: 0.2.0
actors:
  - id: actor_a
    type: human
    label: Actor A
surfaces:
  - id: floor
    label: Floor
relations:
  - id: rel_1
    predicate: standing_on
    subject:
      kind: body_part
      actor: actor_a
      part: foot
      side: left
    object:
      kind: surface
      surface: floor
  - id: rel_2
    predicate: standing_on
    subject:
      kind: body_part
      actor: actor_a
      part: foot
      side: right
    object:
      kind: surface
      surface: floor
```

### Narrative projection (Layer 2)

```
Narrative Projection (non-authoritative):

- Actor A is standing on the floor with both feet.
```

The narrative projection is derived only from the canonical facts above and omits details that are not needed for the current turn.

## Minimal author workflow

1. **Start in Layer 1.** Author the canonical YAML first (actors, objects/surfaces, and relations). Treat it as the single source of truth.
2. **Validate the canonical state.** Ensure the YAML conforms to the schema before using it:

   ```bash
   python tools/validate_examples.py
   ```

3. **Project to Layer 2.** Create a short, turn-appropriate narrative projection that restates only canonical facts and never introduces new ones.

That is the minimal loop: canonical first, validate, then project.
