"""Validate canonical state against schema and semantic checks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema.exceptions import best_match

from .load import load_document

SPATIAL_PREDICATES = {
    "left_of",
    "right_of",
    "above",
    "below",
    "facing",
    "aligned_with",
}

BIDIRECTIONAL_BODY_PART_PREDICATES = {"touching", "contacting"}

SUBJECT_OBJECT_RULES = {
    "gripping": ({"body_part"}, {"object", "anchor"}),
    "holding": ({"body_part"}, {"object", "anchor"}),
    "supporting": ({"surface", "object", "anchor"}, {"body_part"}),
    "standing_on": ({"body_part"}, {"surface", "object", "anchor"}),
    "sitting_on": ({"body_part"}, {"surface", "object", "anchor"}),
    "leaning_on": ({"body_part"}, {"surface", "object", "anchor"}),
}


@dataclass(frozen=True)
class ValidationIssue:
    """A single validation error with a JSON pointer-like path."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_schema() -> dict[str, Any]:
    """Load the bundled JSON Schema."""
    schema_path = resources.files(__package__).joinpath("pose-contact.schema.json")
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _collect_ids(instance: dict[str, Any]) -> dict[str, set[str]]:
    def extract_id(items: list[dict[str, Any]]) -> set[str]:
        return {item["id"] for item in items if isinstance(item, dict) and "id" in item}

    return {
        "actors": extract_id(instance.get("actors", [])),
        "objects": extract_id(instance.get("objects", [])),
        "surfaces": extract_id(instance.get("surfaces", [])),
        "anchors": extract_id(instance.get("anchors", [])),
    }


def _format_path(parts: list[object]) -> str:
    if not parts:
        return "/"
    return "/" + "/".join(str(part) for part in parts)


def _validate_anchor_ownership(
    anchors: list[dict[str, Any]], ids: dict[str, set[str]]
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            continue
        owner_kind = anchor.get("owner_kind")
        owner_id = anchor.get("owner")
        if owner_kind == "object":
            if owner_id not in ids["objects"]:
                issues.append(
                    ValidationIssue(
                        _format_path(["anchors", index, "owner"]),
                        f"unknown object id '{owner_id}'",
                    )
                )
        elif owner_kind == "surface":
            if owner_id not in ids["surfaces"]:
                issues.append(
                    ValidationIssue(
                        _format_path(["anchors", index, "owner"]),
                        f"unknown surface id '{owner_id}'",
                    )
                )
    return issues


def _validate_entity_ref(
    entity: dict[str, Any],
    path: list[object],
    ids: dict[str, set[str]],
) -> tuple[str | None, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    if not isinstance(entity, dict):
        return None, issues
    kind = entity.get("kind")
    if kind == "body_part":
        actor_id = entity.get("actor")
        if actor_id not in ids["actors"]:
            issues.append(
                ValidationIssue(
                    _format_path([*path, "actor"]),
                    f"unknown actor id '{actor_id}'",
                )
            )
    elif kind == "object":
        object_id = entity.get("object")
        if object_id not in ids["objects"]:
            issues.append(
                ValidationIssue(
                    _format_path([*path, "object"]),
                    f"unknown object id '{object_id}'",
                )
            )
    elif kind == "surface":
        surface_id = entity.get("surface")
        if surface_id not in ids["surfaces"]:
            issues.append(
                ValidationIssue(
                    _format_path([*path, "surface"]),
                    f"unknown surface id '{surface_id}'",
                )
            )
    elif kind == "anchor":
        anchor_id = entity.get("anchor")
        if anchor_id not in ids["anchors"]:
            issues.append(
                ValidationIssue(
                    _format_path([*path, "anchor"]),
                    f"unknown anchor id '{anchor_id}'",
                )
            )
    return kind, issues


def _predicate_allows_pairing(
    predicate: str, subject_kind: str | None, object_kind: str | None
) -> bool:
    if subject_kind is None or object_kind is None:
        return True
    if predicate in SPATIAL_PREDICATES:
        return True
    if predicate in BIDIRECTIONAL_BODY_PART_PREDICATES:
        left = {"body_part"}
        right = {"body_part", "object", "surface", "anchor"}
        return (subject_kind in left and object_kind in right) or (
            object_kind in left and subject_kind in right
        )
    if predicate in SUBJECT_OBJECT_RULES:
        allowed_subjects, allowed_objects = SUBJECT_OBJECT_RULES[predicate]
        return subject_kind in allowed_subjects and object_kind in allowed_objects
    return True


def _describe_expected_pairing(predicate: str) -> str:
    if predicate in BIDIRECTIONAL_BODY_PART_PREDICATES:
        return "body_part ↔ body_part/object/surface/anchor"
    if predicate in SUBJECT_OBJECT_RULES:
        allowed_subjects, allowed_objects = SUBJECT_OBJECT_RULES[predicate]
        subject_desc = "/".join(sorted(allowed_subjects))
        object_desc = "/".join(sorted(allowed_objects))
        return f"{subject_desc} → {object_desc}"
    if predicate in SPATIAL_PREDICATES:
        return "any entity reference"
    return "any entity reference"


def _validate_relations(
    relations: list[dict[str, Any]],
    ids: dict[str, set[str]],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        predicate = relation.get("predicate")
        subject = relation.get("subject", {})
        object_ref = relation.get("object", {})
        subject_kind, subject_issues = _validate_entity_ref(
            subject, ["relations", index, "subject"], ids
        )
        object_kind, object_issues = _validate_entity_ref(
            object_ref, ["relations", index, "object"], ids
        )
        issues.extend(subject_issues)
        issues.extend(object_issues)
        if predicate and not _predicate_allows_pairing(
            predicate, subject_kind, object_kind
        ):
            expected = _describe_expected_pairing(predicate)
            issues.append(
                ValidationIssue(
                    _format_path(["relations", index]),
                    f"predicate '{predicate}' requires {expected}",
                )
            )
    return issues


def _normalize_schema_error(error: jsonschema.ValidationError) -> ValidationIssue:
    if error.context:
        error = best_match(error.context)
    path = _format_path(list(error.absolute_path))
    return ValidationIssue(path, error.message)


def validate_instance(
    instance: dict[str, Any], schema: dict[str, Any] | None = None
) -> list[ValidationIssue]:
    """Validate a canonical instance, returning any issues found."""
    schema = schema or load_schema()
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    issues = [_normalize_schema_error(err) for err in validator.iter_errors(instance)]
    issues.sort(key=lambda issue: issue.path)
    if issues:
        return issues

    ids = _collect_ids(instance)
    issues.extend(_validate_anchor_ownership(instance.get("anchors", []), ids))
    issues.extend(_validate_relations(instance.get("relations", []), ids))
    return issues


def validate_document(
    path: str | Path, schema: dict[str, Any] | None = None
) -> list[ValidationIssue]:
    """Load and validate a canonical document."""
    instance = load_document(path)
    if not isinstance(instance, dict):
        return [ValidationIssue("/", "document must be a mapping")]
    return validate_instance(instance, schema=schema)
