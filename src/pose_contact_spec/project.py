"""Generate non-authoritative narrative projections."""

from __future__ import annotations

from typing import Any


def _indexed(items: list[dict[str, Any]], key: str = "id") -> dict[str, dict[str, Any]]:
    return {
        item[key]: item
        for item in items
        if isinstance(item, dict) and key in item
    }


def _describe_entity(
    entity: dict[str, Any],
    actors: dict[str, dict[str, Any]],
    objects: dict[str, dict[str, Any]],
    surfaces: dict[str, dict[str, Any]],
    anchors: dict[str, dict[str, Any]],
) -> str:
    kind = entity.get("kind")
    if kind == "body_part":
        actor_id = entity.get("actor")
        actor = actors.get(actor_id, {})
        actor_label = actor.get("label", actor_id)
        part = entity.get("part")
        side = entity.get("side")
        if side and side != "none":
            part_desc = f"{side} {part}"
        else:
            part_desc = f"{part} (side: {side})" if side else str(part)
        return f"{part_desc} of {actor_label} ({actor_id})"
    if kind == "object":
        object_id = entity.get("object")
        obj = objects.get(object_id, {})
        label = obj.get("label", object_id)
        return f"{label} ({object_id})"
    if kind == "surface":
        surface_id = entity.get("surface")
        surface = surfaces.get(surface_id, {})
        label = surface.get("label", surface_id)
        return f"{label} ({surface_id})"
    if kind == "anchor":
        anchor_id = entity.get("anchor")
        anchor = anchors.get(anchor_id, {})
        name = anchor.get("name", anchor_id)
        role = anchor.get("role")
        owner_kind = anchor.get("owner_kind")
        owner_id = anchor.get("owner")
        owner_label = owner_id
        if owner_kind == "object":
            owner_label = objects.get(owner_id, {}).get("label", owner_id)
        elif owner_kind == "surface":
            owner_label = surfaces.get(owner_id, {}).get("label", owner_id)
        role_note = f", role: {role}" if role else ""
        return f"{name} ({anchor_id}) on {owner_label} ({owner_id}){role_note}"
    return "unknown entity"


def _format_qualifiers(qualifiers: dict[str, Any] | None) -> str:
    if not qualifiers:
        return ""
    parts = [f"{key}={qualifiers[key]}" for key in sorted(qualifiers)]
    return f" (qualifiers: {', '.join(parts)})"


def project_narrative(instance: dict[str, Any]) -> str:
    """Create a minimal narrative projection from canonical state."""
    actors = _indexed(instance.get("actors", []))
    objects = _indexed(instance.get("objects", []))
    surfaces = _indexed(instance.get("surfaces", []))
    anchors = _indexed(instance.get("anchors", []))

    lines = ["Narrative Projection (non-authoritative):", ""]
    for relation in instance.get("relations", []):
        if not isinstance(relation, dict):
            continue
        predicate = relation.get("predicate", "relation")
        subject = relation.get("subject", {})
        object_ref = relation.get("object", {})
        subject_desc = _describe_entity(subject, actors, objects, surfaces, anchors)
        object_desc = _describe_entity(object_ref, actors, objects, surfaces, anchors)
        verb = predicate.replace("_", " ")
        qualifiers = _format_qualifiers(relation.get("qualifiers"))
        lines.append(f"- {subject_desc} is {verb} {object_desc}.{qualifiers}")

    lines.append("")
    lines.append(
        "Notes: This projection is derived from canonical state and MUST NOT be treated "
        "as authoritative."
    )
    return "\n".join(lines)
