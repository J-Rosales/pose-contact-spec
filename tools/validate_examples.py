#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
from jsonschema.exceptions import best_match
import yaml

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


def load_schema(schema_path: Path) -> dict:
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_example(example_path: Path) -> object:
    if example_path.suffix == ".json":
        with example_path.open(encoding="utf-8") as handle:
            return json.load(handle)
    with example_path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def collect_ids(instance: dict) -> dict[str, set[str]]:
    def extract_id(items: list[dict]) -> set[str]:
        return {item["id"] for item in items if isinstance(item, dict) and "id" in item}

    return {
        "actors": extract_id(instance.get("actors", [])),
        "objects": extract_id(instance.get("objects", [])),
        "surfaces": extract_id(instance.get("surfaces", [])),
        "anchors": extract_id(instance.get("anchors", [])),
    }


def format_path(parts: list[object]) -> str:
    if not parts:
        return "/"
    return "/" + "/".join(str(part) for part in parts)


def validate_anchor_ownership(
    anchors: list[dict], ids: dict[str, set[str]]
) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            continue
        owner_kind = anchor.get("owner_kind")
        owner_id = anchor.get("owner")
        if owner_kind == "object":
            if owner_id not in ids["objects"]:
                errors.append(
                    (
                        format_path(["anchors", index, "owner"]),
                        f"unknown object id '{owner_id}'",
                    )
                )
        elif owner_kind == "surface":
            if owner_id not in ids["surfaces"]:
                errors.append(
                    (
                        format_path(["anchors", index, "owner"]),
                        f"unknown surface id '{owner_id}'",
                    )
                )
    return errors


def validate_entity_ref(
    entity: dict,
    path: list[object],
    ids: dict[str, set[str]],
) -> tuple[str | None, list[tuple[str, str]]]:
    errors: list[tuple[str, str]] = []
    if not isinstance(entity, dict):
        return None, errors
    kind = entity.get("kind")
    if kind == "body_part":
        actor_id = entity.get("actor")
        if actor_id not in ids["actors"]:
            errors.append(
                (
                    format_path([*path, "actor"]),
                    f"unknown actor id '{actor_id}'",
                )
            )
    elif kind == "object":
        object_id = entity.get("object")
        if object_id not in ids["objects"]:
            errors.append(
                (
                    format_path([*path, "object"]),
                    f"unknown object id '{object_id}'",
                )
            )
    elif kind == "surface":
        surface_id = entity.get("surface")
        if surface_id not in ids["surfaces"]:
            errors.append(
                (
                    format_path([*path, "surface"]),
                    f"unknown surface id '{surface_id}'",
                )
            )
    elif kind == "anchor":
        anchor_id = entity.get("anchor")
        if anchor_id not in ids["anchors"]:
            errors.append(
                (
                    format_path([*path, "anchor"]),
                    f"unknown anchor id '{anchor_id}'",
                )
            )
    return kind, errors


def predicate_allows_pairing(
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


def describe_expected_pairing(predicate: str) -> str:
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


def validate_relations(
    relations: list[dict],
    ids: dict[str, set[str]],
) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        predicate = relation.get("predicate")
        subject = relation.get("subject", {})
        object_ref = relation.get("object", {})
        subject_kind, subject_errors = validate_entity_ref(
            subject, ["relations", index, "subject"], ids
        )
        object_kind, object_errors = validate_entity_ref(
            object_ref, ["relations", index, "object"], ids
        )
        errors.extend(subject_errors)
        errors.extend(object_errors)
        if predicate and not predicate_allows_pairing(
            predicate, subject_kind, object_kind
        ):
            expected = describe_expected_pairing(predicate)
            errors.append(
                (
                    format_path(["relations", index]),
                    f"predicate '{predicate}' requires {expected}",
                )
            )
    return errors


def normalize_schema_error(error: jsonschema.ValidationError) -> tuple[str, str]:
    if error.context:
        error = best_match(error.context)
    path = format_path(list(error.absolute_path))
    return path, error.message


def validate_examples(schema: dict, examples_dir: Path) -> list[str]:
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    errors: list[str] = []
    for example_path in sorted(examples_dir.iterdir()):
        if example_path.suffix not in {".yaml", ".yml", ".json"}:
            continue
        instance = load_example(example_path)
        schema_errors = [
            normalize_schema_error(err) for err in validator.iter_errors(instance)
        ]
        schema_errors.sort()
        if schema_errors:
            for path, message in schema_errors:
                errors.append(f"{example_path.name}: {path}: {message}")
            continue

        if isinstance(instance, dict):
            ids = collect_ids(instance)
            anchors = instance.get("anchors", [])
            relations = instance.get("relations", [])

            for path, message in validate_anchor_ownership(anchors, ids):
                errors.append(f"{example_path.name}: {path}: {message}")
            for path, message in validate_relations(relations, ids):
                errors.append(f"{example_path.name}: {path}: {message}")
    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = repo_root / "schema" / "pose-contact.schema.json"
    examples_dir = repo_root / "examples"

    schema = load_schema(schema_path)
    errors = validate_examples(schema, examples_dir)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("All examples are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
