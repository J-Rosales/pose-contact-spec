#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


def load_schema(schema_path: Path) -> dict:
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_example(example_path: Path) -> object:
    if example_path.suffix == ".json":
        with example_path.open(encoding="utf-8") as handle:
            return json.load(handle)
    with example_path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_examples(schema: dict, examples_dir: Path) -> list[str]:
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    errors: list[str] = []
    for example_path in sorted(examples_dir.iterdir()):
        if example_path.suffix not in {".yaml", ".yml", ".json"}:
            continue
        instance = load_example(example_path)
        file_errors = sorted(validator.iter_errors(instance), key=str)
        if file_errors:
            for error in file_errors:
                location = "/".join(str(part) for part in error.path) or "<root>"
                errors.append(
                    f"{example_path.name}: {location}: {error.message}"
                )
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
