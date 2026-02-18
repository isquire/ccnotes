"""Constraint functions for meal plan generation."""

from __future__ import annotations

from recipe_planner.models.recipe import Recipe


def no_same_recipe_consecutive(
    partial_plan: dict[str, dict[str, str]],
    candidate_title: str,
    day: str,
    meal_type: str,
) -> bool:
    """Reject if the same recipe was used in the previous day's same meal slot."""
    day_order = [
        "Saturday", "Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Next Sunday",
    ]
    try:
        idx = day_order.index(day)
    except ValueError:
        return True

    if idx == 0:
        return True

    prev_day = day_order[idx - 1]
    prev_meals = partial_plan.get(prev_day, {})
    prev_recipe = prev_meals.get(meal_type)

    return prev_recipe != candidate_title


def no_same_cuisine_consecutive(
    partial_plan: dict[str, dict[str, str]],
    candidate_cuisine: str,
    day: str,
    cuisine_map: dict[str, str],
) -> bool:
    """Reject if same cuisine was used for dinner the previous day."""
    day_order = [
        "Saturday", "Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Next Sunday",
    ]
    try:
        idx = day_order.index(day)
    except ValueError:
        return True

    if idx == 0:
        return True

    prev_day = day_order[idx - 1]
    prev_dinner = partial_plan.get(prev_day, {}).get("dinner", "")
    prev_cuisine = cuisine_map.get(prev_dinner, "")

    return prev_cuisine != candidate_cuisine


def no_repeat_within_days(
    partial_plan: dict[str, dict[str, str]],
    candidate_title: str,
    window: int = 3,
) -> bool:
    """Reject if the recipe was used in the plan within the last N days."""
    all_used = []
    for day_meals in partial_plan.values():
        for recipe_title in day_meals.values():
            all_used.append(recipe_title)

    # Check last `window * 3` meals (3 meals per day)
    recent = all_used[-(window * 3):]
    return candidate_title not in recent
