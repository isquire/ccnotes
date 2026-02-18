"""Undo/redo support via version history traversal."""

from __future__ import annotations

from recipe_planner.models.recipe import Recipe
from recipe_planner.editor.version_manager import jump_to_version


class UndoRedoManager:
    """Manages undo/redo state per recipe using version history."""

    def __init__(self):
        # Maps recipe_id -> current position in version history
        self._positions: dict[str, int] = {}

    def track(self, recipe: Recipe) -> None:
        """Update tracking to the recipe's current version."""
        self._positions[recipe.id] = len(recipe.version_history) - 1

    def can_undo(self, recipe: Recipe) -> bool:
        pos = self._positions.get(recipe.id, len(recipe.version_history) - 1)
        return pos > 0

    def can_redo(self, recipe: Recipe) -> bool:
        pos = self._positions.get(recipe.id, len(recipe.version_history) - 1)
        return pos < len(recipe.version_history) - 1

    def undo(self, recipe: Recipe) -> Recipe:
        """Revert to the previous version."""
        if not self.can_undo(recipe):
            raise ValueError("Nothing to undo")

        pos = self._positions.get(recipe.id, len(recipe.version_history) - 1)
        target_pos = pos - 1
        target_version = recipe.version_history[target_pos].version

        recipe = jump_to_version(recipe, target_version)
        # After jump_to_version, a new entry is appended. Track the target position.
        self._positions[recipe.id] = target_pos
        return recipe

    def redo(self, recipe: Recipe) -> Recipe:
        """Move forward to the next version (if available)."""
        if not self.can_redo(recipe):
            raise ValueError("Nothing to redo")

        pos = self._positions.get(recipe.id, len(recipe.version_history) - 1)
        target_pos = pos + 1
        target_version = recipe.version_history[target_pos].version

        recipe = jump_to_version(recipe, target_version)
        self._positions[recipe.id] = target_pos
        return recipe


# Module-level singleton for convenience
_manager = UndoRedoManager()


def track_recipe(recipe: Recipe) -> None:
    _manager.track(recipe)


def undo(recipe: Recipe) -> Recipe:
    return _manager.undo(recipe)


def redo(recipe: Recipe) -> Recipe:
    return _manager.redo(recipe)


def can_undo(recipe: Recipe) -> bool:
    return _manager.can_undo(recipe)


def can_redo(recipe: Recipe) -> bool:
    return _manager.can_redo(recipe)
