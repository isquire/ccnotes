"""Meal plan repository — CRUD operations against SQLite."""

from __future__ import annotations

import json
import sqlite3
from typing import Optional

from recipe_planner.models.meal_plan import MealPlan


def _row_to_plan(row: sqlite3.Row) -> MealPlan:
    data = dict(row)
    data["days"] = json.loads(data["days"])
    data["recipes_used"] = json.loads(data["recipes_used"])
    data["metadata"] = json.loads(data["metadata"])
    return MealPlan.from_dict(data)


def save_meal_plan(conn: sqlite3.Connection, plan: MealPlan) -> MealPlan:
    conn.execute(
        """INSERT OR REPLACE INTO meal_plans
           (id, start_date, end_date, days, recipes_used, metadata)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            plan.id,
            plan.start_date,
            plan.end_date,
            json.dumps(plan.days),
            json.dumps(plan.recipes_used),
            json.dumps(plan.metadata),
        ),
    )
    return plan


def get_meal_plan(conn: sqlite3.Connection, plan_id: str) -> Optional[MealPlan]:
    cursor = conn.execute("SELECT * FROM meal_plans WHERE id = ?", (plan_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    return _row_to_plan(row)


def list_meal_plans(conn: sqlite3.Connection) -> list[MealPlan]:
    cursor = conn.execute(
        "SELECT * FROM meal_plans ORDER BY start_date DESC"
    )
    return [_row_to_plan(row) for row in cursor.fetchall()]


def delete_meal_plan(conn: sqlite3.Connection, plan_id: str) -> bool:
    cursor = conn.execute("DELETE FROM meal_plans WHERE id = ?", (plan_id,))
    return cursor.rowcount > 0
