# Terminology

This section is normative unless otherwise noted.

## Definitions

- **Actor:** An entity capable of having articulated body parts. In this specification, actors are human by default.
- **Body Part:** A named anatomical segment belonging to an actor. Body parts are referenced with explicit side disambiguation.
- **Contact:** A relation indicating physical contact between two entities without implying support or force.
- **Support:** A relation indicating that one entity bears the weight of another.
- **Relation:** A typed predicate connecting a subject entity to an object entity.
- **Predicate:** The controlled vocabulary term that defines the semantics of a relation.
- **Canonical State:** The authoritative, lossless, machine-validated representation of pose and contact facts.
- **Narrative Projection:** A non-authoritative, derived representation of selected canonical facts for language-model context.

## Left/Right Disambiguation

Body parts that occur in left/right pairs MUST include a `side` attribute with a value of `left` or `right`. Unpaired parts MUST use `none`. Implementations MUST NOT infer side from naming conventions.

