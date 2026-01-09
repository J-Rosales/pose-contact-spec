# Relations

This section is normative.

## Predicate Vocabulary

The following predicates are exhaustive and mutually independent. Implementations MUST reject predicates outside this list.

| Predicate | Meaning | Does NOT Imply |
| --- | --- | --- |
| `touching` | Subject is in physical contact with object. | Support or grip strength. |
| `gripping` | Subject applies a grasping contact. | Lifting or support. |
| `holding` | Subject maintains control of an object. | Gripping or support. |
| `supporting` | Object bears the weight of subject. | Full-body support. |
| `standing_on` | Subject is upright on a surface. | Motion or balance details. |
| `sitting_on` | Subject is seated on a surface/object. | Support by other parts. |
| `leaning_on` | Subject uses object for partial support. | Full support. |
| `contacting` | Synonym for touching when specificity is not required. | Any specific interaction mode. |
| `left_of` | Subject is spatially left of object. | Contact. |
| `right_of` | Subject is spatially right of object. | Contact. |
| `above` | Subject is spatially above object. | Support or contact. |
| `below` | Subject is spatially below object. | Support or contact. |
| `facing` | Subject is oriented toward object. | Contact or alignment. |
| `aligned_with` | Subject is aligned with object axis. | Contact or facing. |

## Allowed Pairings

Relations MUST use subject and object entity references as follows:

- `touching`, `contacting`: body_part ↔ body_part/object/surface
- `gripping`, `holding`: body_part → object
- `supporting`: surface/object → body_part
- `standing_on`, `sitting_on`, `leaning_on`: body_part → surface/object
- Spatial relations (`left_of`, `right_of`, `above`, `below`, `facing`, `aligned_with`): any entity reference

## Qualifiers

Qualifiers are optional and MUST NOT change predicate semantics. Allowed qualifiers:

- `intensity`: `light` or `firm`.
- `duration_ms`: non-negative integer.
- `contact_area`: free-form string.

