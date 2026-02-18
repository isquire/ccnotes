"""Build a raw ingredient list from a meal plan."""

from __future__ import annotations

import sqlite3
from typing import Optional

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.meal_plan import MealPlan
from recipe_planner.models.recipe import Recipe
from recipe_planner.db.repositories.recipe_repo import get_recipe_by_title


def collect_ingredients(
    plan: MealPlan,
    conn: sqlite3.Connection,
) -> list[Ingredient]:
    """Walk every slot in a meal plan and collect all ingredients.

    Args:
        plan: The meal plan to process.
        conn: Database connection to look up recipes.

    Returns:
        Flat list of all Ingredient objects across all meals.
    """
    all_ingredients: list[Ingredient] = []

    for day_name, meals in plan.days.items():
        for meal_type, recipe_title in meals.items():
            recipe = get_recipe_by_title(conn, recipe_title)
            if recipe:
                for ing in recipe.ingredients:
                    all_ingredients.append(ing)

    return all_ingredients


def collect_recipe_titles(plan: MealPlan) -> list[str]:
    """Get unique recipe titles used in a meal plan."""
    titles = set()
    for meals in plan.days.values():
        for recipe_title in meals.values():
            titles.add(recipe_title)
    return sorted(titles)
