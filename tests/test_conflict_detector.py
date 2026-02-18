"""Tests for multi-device conflict detection."""

from recipe_planner.editor.conflict_detector import (
    detect_conflict,
    resolve_conflict,
)


def test_no_conflict_when_versions_match():
    server = {"version": 3, "title": "Pasta", "cuisine": "Italian"}
    client = {"version": 3, "title": "Pasta", "cuisine": "Italian"}
    changes = {"title": "New Pasta"}

    result = detect_conflict(server, client, changes)
    assert result is None


def test_no_conflict_different_fields():
    server = {"version": 4, "title": "Updated Pasta", "cuisine": "Italian"}
    client = {"version": 3, "title": "Pasta", "cuisine": "Italian"}
    changes = {"cuisine": "Mediterranean"}  # Different field than what server changed

    result = detect_conflict(server, client, changes)
    assert result is None


def test_conflict_detected_same_field():
    server = {"version": 4, "title": "Server Title", "cuisine": "Italian"}
    client = {"version": 3, "title": "Old Title", "cuisine": "Italian"}
    changes = {"title": "Client Title"}

    result = detect_conflict(server, client, changes)
    assert result is not None
    assert result["conflict_detected"] is True
    assert result["server_version"] == 4
    assert result["client_version"] == 3
    assert "title" in result["conflicts"]


def test_resolve_keep_server():
    server = {"version": 4, "title": "Server Title", "cuisine": "Italian"}
    changes = {"title": "Client Title", "cuisine": "Mexican"}
    conflicts = {
        "conflicts": {"title": {"client_value": "Client Title", "server_value": "Server Title"}}
    }

    resolved = resolve_conflict(server, changes, conflicts, "keep_server")
    assert "title" not in resolved
    assert resolved.get("cuisine") == "Mexican"


def test_resolve_keep_client():
    server = {"version": 4, "title": "Server Title"}
    changes = {"title": "Client Title"}
    conflicts = {
        "conflicts": {"title": {"client_value": "Client Title", "server_value": "Server Title"}}
    }

    resolved = resolve_conflict(server, changes, conflicts, "keep_client")
    assert resolved["title"] == "Client Title"
