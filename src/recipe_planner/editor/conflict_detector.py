"""Multi-device conflict detection using optimistic locking."""

from __future__ import annotations

from typing import Any


class ConflictError(Exception):
    """Raised when a version conflict is detected."""

    def __init__(self, conflict_info: dict):
        self.conflict_info = conflict_info
        super().__init__(f"Version conflict detected: {conflict_info}")


def detect_conflict(
    server_recipe: dict,
    client_recipe: dict,
    client_changes: dict,
) -> dict | None:
    """Detect if there's a conflict between client and server versions.

    Args:
        server_recipe: Current recipe state on the server (from DB).
        client_recipe: Recipe state the client loaded before editing.
        client_changes: The fields the client wants to change.

    Returns:
        Conflict info dict if conflict detected, None otherwise.
    """
    server_version = server_recipe.get("version", 1)
    client_version = client_recipe.get("version", 1)

    if client_version >= server_version:
        return None  # No conflict

    # Find conflicting fields
    conflicts = {}
    for field_name in client_changes:
        server_val = server_recipe.get(field_name)
        client_base_val = client_recipe.get(field_name)
        if server_val != client_base_val:
            conflicts[field_name] = {
                "client_value": client_changes[field_name],
                "server_value": server_val,
            }

    if not conflicts:
        return None  # Different fields edited — no real conflict

    return {
        "conflict_detected": True,
        "server_version": server_version,
        "client_version": client_version,
        "conflicts": conflicts,
        "resolution_options": [
            "keep_server",
            "keep_client",
            "merge_if_possible",
        ],
    }


def resolve_conflict(
    server_recipe: dict,
    client_changes: dict,
    conflicts: dict,
    resolution: str,
) -> dict:
    """Apply a conflict resolution strategy.

    Args:
        server_recipe: Current server-side recipe snapshot.
        client_changes: Changes the client wants to apply.
        conflicts: The conflicts dict from detect_conflict.
        resolution: One of 'keep_server', 'keep_client', 'merge_if_possible'.

    Returns:
        Dict of changes to apply.
    """
    conflict_fields = set(conflicts.get("conflicts", {}).keys())

    if resolution == "keep_server":
        # Drop client changes for conflicting fields
        return {
            k: v for k, v in client_changes.items()
            if k not in conflict_fields
        }

    elif resolution == "keep_client":
        # Apply all client changes
        return dict(client_changes)

    elif resolution == "merge_if_possible":
        # Keep client changes for non-conflicting fields,
        # keep server values for conflicting fields
        merged = {}
        for k, v in client_changes.items():
            if k not in conflict_fields:
                merged[k] = v
            # Conflicting fields keep server value (already in place)
        return merged

    else:
        raise ValueError(f"Unknown resolution strategy: {resolution}")
