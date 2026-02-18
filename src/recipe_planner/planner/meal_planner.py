"""Weekly meal plan generator (Saturday to following Sunday, 8 days)."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from recipe_planner.models.meal_plan import MealPlan
from recipe_planner.models.recipe import Recipe
from recipe_planner.planner.constraints import (
    no_repeat_within_days,
    no_same_recipe_consecutive,
)
from recipe_planner.planner.slot_filler import fill_slot


DAY_ORDER = [
    "Saturday", "Sunday", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday", "Next Sunday",
]

MEAL_TYPES = ["breakfast", "lunch", "dinner"]


def generate_meal_plan(
    recipes: list[Recipe],
    start_date: str | None = None,
) -> MealPlan:
    """Generate an 8-day meal plan from a pool of recipes.

    Args:
        recipes: Available recipes to choose from.
        start_date: Optional start date (YYYY-MM-DD). Defaults to next Saturday.

    Returns:
        A populated MealPlan object.
    """
    if not recipes:
        raise ValueError("Cannot generate a meal plan with no recipes")

    # Determine dates
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = _next_saturday()

    end = start + timedelta(days=7)

    # Build cuisine map for constraint checking
    cuisine_map = {r.title: r.cuisine for r in recipes}

    # Define constraints
    constraints = [
        lambda partial_plan, candidate_title, day, meal_type, **kw: (
            no_same_recipe_consecutive(partial_plan, candidate_title, day, meal_type)
        ),
        lambda partial_plan, candidate_title, **kw: (
            no_repeat_within_days(partial_plan, candidate_title, window=2)
        ),
    ]

    # Fill the plan day by day
    days: dict[str, dict[str, str]] = {}
    recipes_used: list[str] = []

    for day_name in DAY_ORDER:
        day_meals: dict[str, str] = {}
        for meal_type in MEAL_TYPES:
            selected = fill_slot(
                candidates=recipes,
                partial_plan=days,
                day=day_name,
                meal_type=meal_type,
                constraints=constraints,
                cuisine_map=cuisine_map,
            )
            if selected:
                day_meals[meal_type] = selected
                if selected not in recipes_used:
                    recipes_used.append(selected)
        days[day_name] = day_meals

    plan = MealPlan(
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        days=days,
        recipes_used=recipes_used,
        metadata={
            "generated_on": datetime.now().strftime("%Y-%m-%d"),
            "notes": [f"Generated from {len(recipes)} available recipes"],
        },
    )

    return plan


def _next_saturday() -> datetime:
    """Find the next Saturday from today."""
    today = datetime.now()
    days_ahead = 5 - today.weekday()  # Saturday = 5
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)
