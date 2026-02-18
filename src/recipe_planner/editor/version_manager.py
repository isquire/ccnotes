"""Version management for recipes — create, diff, restore versions."""

from __future__ import annotations

import copy
from datetime import datetime

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe, VersionEntry
from recipe_planner.editor.field_tracker import diff_snapshots, compute_edited_fields


def apply_edit(recipe: Recipe, changes: dict) -> Recipe:
    """Apply a dict of field changes to a recipe, updating version tracking.

    `changes` is a dict like {"title": "New Title", "cuisine": "Italian"}.
    Only explicitly provided fields are modified.
    Returns the updated recipe.
    """
    old_snapshot = recipe.snapshot()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Apply changes
    for field_name, value in changes.items():
        if field_name == "ingredients" and isinstance(value, list):
            recipe.ingredients = [
                Ingredient.from_dict(i) if isinstance(i, dict) else i
                for i in value
            ]
        elif field_name == "instructions" and isinstance(value, list):
            recipe.instructions = list(value)
        elif field_name == "tags" and isinstance(value, list):
            recipe.tags = list(value)
        elif hasattr(recipe, field_name):
            setattr(recipe, field_name, value)

    # Increment version and update timestamp
    recipe.version += 1
    recipe.date_modified = now

    # Compute change highlights
    new_snapshot = recipe.snapshot()
    recipe.change_highlights = diff_snapshots(old_snapshot, new_snapshot)

    # Update edited_fields based on diff from original_values
    recipe.edited_fields = compute_edited_fields(
        recipe.original_values, new_snapshot
    )

    # Append version history entry
    change_descriptions = [
        f"Modified {field}" for field in recipe.change_highlights
    ]
    recipe.version_history.append(
        VersionEntry(
            version=recipe.version,
            timestamp=now,
            changes=change_descriptions,
            snapshot=new_snapshot,
        )
    )

    return recipe


def restore_field(recipe: Recipe, field_name: str) -> Recipe:
    """Restore a single field to its original value."""
    if field_name not in recipe.original_values:
        raise ValueError(f"No original value stored for field '{field_name}'")

    original_val = copy.deepcopy(recipe.original_values[field_name])
    return apply_edit(recipe, {field_name: original_val})


def restore_fields(recipe: Recipe, field_names: list[str]) -> Recipe:
    """Restore multiple fields to their original values."""
    changes = {}
    for field_name in field_names:
        if field_name not in recipe.original_values:
            raise ValueError(f"No original value stored for field '{field_name}'")
        changes[field_name] = copy.deepcopy(recipe.original_values[field_name])
    return apply_edit(recipe, changes)


def restore_all(recipe: Recipe) -> Recipe:
    """Restore all fields to original values."""
    return apply_edit(recipe, copy.deepcopy(recipe.original_values))


def get_version_snapshot(recipe: Recipe, version_number: int) -> dict | None:
    """Retrieve the snapshot for a specific version number."""
    for entry in recipe.version_history:
        if entry.version == version_number:
            return copy.deepcopy(entry.snapshot)
    return None


def jump_to_version(recipe: Recipe, version_number: int) -> Recipe:
    """Replace the current recipe state with the snapshot of a specific version."""
    snapshot = get_version_snapshot(recipe, version_number)
    if snapshot is None:
        raise ValueError(f"Version {version_number} not found in history")

    changes = {
        "title": snapshot.get("title", recipe.title),
        "cuisine": snapshot.get("cuisine", recipe.cuisine),
        "ingredients": snapshot.get("ingredients", []),
        "instructions": snapshot.get("instructions", []),
        "prep_time": snapshot.get("prep_time"),
        "cook_time": snapshot.get("cook_time"),
        "tags": snapshot.get("tags", []),
    }
    return apply_edit(recipe, changes)
