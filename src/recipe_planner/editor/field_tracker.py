"""Field-level change tracking between recipe snapshots."""

from __future__ import annotations

import copy
from typing import Any


def diff_snapshots(old: dict, new: dict) -> dict[str, dict[str, Any]]:
    """Compare two recipe snapshots and return field-level diffs.

    Returns a dict of field_name -> {"before": ..., "after": ...} for changed fields.
    """
    changes: dict[str, dict[str, Any]] = {}
    trackable_fields = [
        "title", "cuisine", "ingredients", "instructions",
        "prep_time", "cook_time", "tags",
    ]

    for field_name in trackable_fields:
        old_val = old.get(field_name)
        new_val = new.get(field_name)
        if old_val != new_val:
            changes[field_name] = {
                "before": copy.deepcopy(old_val),
                "after": copy.deepcopy(new_val),
            }

    return changes


def compute_edited_fields(original_values: dict, current_snapshot: dict) -> list[str]:
    """Determine which fields currently differ from the original values."""
    edited = []
    for field_name in original_values:
        if field_name in current_snapshot:
            if original_values[field_name] != current_snapshot[field_name]:
                edited.append(field_name)
    return edited
