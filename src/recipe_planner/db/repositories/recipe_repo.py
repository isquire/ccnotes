"""Recipe repository — CRUD operations against SQLite."""

from __future__ import annotations

import json
import sqlite3
from typing import Optional

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe, VersionEntry


def _row_to_recipe(row: sqlite3.Row) -> Recipe:
    """Convert a database row to a Recipe object."""
    data = dict(row)
    data["ingredients"] = json.loads(data["ingredients"])
    data["instructions"] = json.loads(data["instructions"])
    data["tags"] = json.loads(data["tags"])
    data["confidence_notes"] = json.loads(data["confidence_notes"])
    data["original_values"] = json.loads(data["original_values"])
    data["edited_fields"] = json.loads(data["edited_fields"])
    data["version_history"] = json.loads(data["version_history"])
    data["change_highlights"] = json.loads(data["change_highlights"])
    return Recipe.from_dict(data)


def save_recipe(conn: sqlite3.Connection, recipe: Recipe) -> Recipe:
    """Insert or replace a recipe in the database."""
    conn.execute(
        """INSERT OR REPLACE INTO recipes
           (id, version, title, cuisine, ingredients, instructions,
            prep_time, cook_time, tags, confidence_notes,
            date_added, date_modified, last_used_in_meal_plan, times_used,
            original_values, edited_fields, version_history, change_highlights)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            recipe.id,
            recipe.version,
            recipe.title,
            recipe.cuisine,
            json.dumps([i.to_dict() for i in recipe.ingredients]),
            json.dumps(recipe.instructions),
            recipe.prep_time,
            recipe.cook_time,
            json.dumps(recipe.tags),
            json.dumps(recipe.confidence_notes),
            recipe.date_added,
            recipe.date_modified,
            recipe.last_used_in_meal_plan,
            recipe.times_used,
            json.dumps(recipe.original_values),
            json.dumps(recipe.edited_fields),
            json.dumps([v.to_dict() for v in recipe.version_history]),
            json.dumps(recipe.change_highlights),
        ),
    )
    return recipe


def get_recipe(conn: sqlite3.Connection, recipe_id: str) -> Optional[Recipe]:
    """Retrieve a recipe by ID."""
    cursor = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    return _row_to_recipe(row)


def get_recipe_by_title(conn: sqlite3.Connection, title: str) -> Optional[Recipe]:
    """Retrieve a recipe by exact title match (case-insensitive)."""
    cursor = conn.execute(
        "SELECT * FROM recipes WHERE LOWER(title) = LOWER(?)", (title,)
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return _row_to_recipe(row)


def list_recipes(
    conn: sqlite3.Connection,
    cuisine: Optional[str] = None,
    tag: Optional[str] = None,
    order_by: str = "date_added",
) -> list[Recipe]:
    """List recipes with optional filters."""
    query = "SELECT * FROM recipes WHERE 1=1"
    params: list = []

    if cuisine:
        query += " AND LOWER(cuisine) = LOWER(?)"
        params.append(cuisine)

    if tag:
        query += " AND tags LIKE ?"
        params.append(f'%"{tag}"%')

    valid_orders = {
        "date_added": "date_added DESC",
        "date_modified": "date_modified DESC",
        "title": "title ASC",
        "last_used": "last_used_in_meal_plan DESC",
        "times_used": "times_used DESC",
    }
    query += f" ORDER BY {valid_orders.get(order_by, 'date_added DESC')}"

    cursor = conn.execute(query, params)
    return [_row_to_recipe(row) for row in cursor.fetchall()]


def search_recipes(conn: sqlite3.Connection, search_term: str) -> list[Recipe]:
    """Search recipes by title or ingredients (partial match)."""
    pattern = f"%{search_term}%"
    cursor = conn.execute(
        """SELECT * FROM recipes
           WHERE title LIKE ? OR ingredients LIKE ?
           ORDER BY date_modified DESC""",
        (pattern, pattern),
    )
    return [_row_to_recipe(row) for row in cursor.fetchall()]


def delete_recipe(conn: sqlite3.Connection, recipe_id: str) -> bool:
    """Delete a recipe by ID. Returns True if a row was deleted."""
    cursor = conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    return cursor.rowcount > 0


def get_recently_used(conn: sqlite3.Connection, limit: int = 10) -> list[Recipe]:
    """Get recipes most recently used in a meal plan."""
    cursor = conn.execute(
        "SELECT * FROM recipes WHERE last_used_in_meal_plan IS NOT NULL "
        "ORDER BY last_used_in_meal_plan DESC LIMIT ?",
        (limit,),
    )
    return [_row_to_recipe(row) for row in cursor.fetchall()]
