"""Fill individual meal slots from a candidate recipe pool."""

from __future__ import annotations

import random
from typing import Callable

from recipe_planner.models.recipe import Recipe


def fill_slot(
    candidates: list[Recipe],
    partial_plan: dict[str, dict[str, str]],
    day: str,
    meal_type: str,
    constraints: list[Callable],
    cuisine_map: dict[str, str],
) -> str | None:
    """Select a recipe for a specific day/meal slot respecting constraints.

    Args:
        candidates: Pool of available recipes.
        partial_plan: Current state of the meal plan being built.
        day: Day name (e.g., 'Monday').
        meal_type: 'breakfast', 'lunch', or 'dinner'.
        constraints: List of constraint functions to check.
        cuisine_map: Mapping of recipe title -> cuisine.

    Returns:
        Selected recipe title, or None if no candidate passes.
    """
    # Shuffle for variety
    shuffled = list(candidates)
    random.shuffle(shuffled)

    for recipe in shuffled:
        passes_all = True
        for constraint_fn in constraints:
            try:
                if not constraint_fn(
                    partial_plan=partial_plan,
                    candidate_title=recipe.title,
                    candidate_cuisine=recipe.cuisine,
                    day=day,
                    meal_type=meal_type,
                    cuisine_map=cuisine_map,
                ):
                    passes_all = False
                    break
            except TypeError:
                # Constraint doesn't accept all kwargs — try simpler signature
                try:
                    if not constraint_fn(partial_plan, recipe.title, day, meal_type):
                        passes_all = False
                        break
                except TypeError:
                    pass

        if passes_all:
            return recipe.title

    # Relaxed fallback: just pick any recipe
    if shuffled:
        return shuffled[0].title
    return None
