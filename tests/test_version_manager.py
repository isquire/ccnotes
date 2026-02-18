"""Tests for version management — edit, restore, and version jumping."""

from recipe_planner.editor.version_manager import (
    apply_edit,
    jump_to_version,
    restore_all,
    restore_field,
)


def test_apply_edit_increments_version(sample_recipe):
    assert sample_recipe.version == 1
    updated = apply_edit(sample_recipe, {"title": "Updated Bolognese"})
    assert updated.version == 2
    assert updated.title == "Updated Bolognese"


def test_apply_edit_tracks_change_highlights(sample_recipe):
    updated = apply_edit(sample_recipe, {"title": "New Title"})
    assert "title" in updated.change_highlights
    assert updated.change_highlights["title"]["before"] == "Classic Spaghetti Bolognese"
    assert updated.change_highlights["title"]["after"] == "New Title"


def test_apply_edit_updates_edited_fields(sample_recipe):
    updated = apply_edit(sample_recipe, {"title": "New Title"})
    assert "title" in updated.edited_fields


def test_apply_edit_appends_version_history(sample_recipe):
    initial_count = len(sample_recipe.version_history)
    updated = apply_edit(sample_recipe, {"cuisine": "American"})
    assert len(updated.version_history) == initial_count + 1


def test_restore_field(sample_recipe):
    modified = apply_edit(sample_recipe, {"title": "Changed Title"})
    assert modified.title == "Changed Title"

    restored = restore_field(modified, "title")
    assert restored.title == "Classic Spaghetti Bolognese"
    assert "title" not in restored.edited_fields


def test_restore_all(sample_recipe):
    modified = apply_edit(sample_recipe, {"title": "New", "cuisine": "American"})
    restored = restore_all(modified)
    assert restored.title == "Classic Spaghetti Bolognese"
    assert restored.cuisine == "Italian"


def test_jump_to_version(sample_recipe):
    v1_title = sample_recipe.title
    modified = apply_edit(sample_recipe, {"title": "V2 Title"})
    modified = apply_edit(modified, {"title": "V3 Title"})

    jumped = jump_to_version(modified, 1)
    assert jumped.title == v1_title


def test_multiple_edits_preserve_original(sample_recipe):
    r = apply_edit(sample_recipe, {"title": "Edit 1"})
    r = apply_edit(r, {"title": "Edit 2"})
    r = apply_edit(r, {"title": "Edit 3"})

    # Original should never change
    assert r.original_values["title"] == "Classic Spaghetti Bolognese"
    assert r.version == 4  # 1 + 3 edits
