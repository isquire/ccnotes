"""Shopping list repository — CRUD operations against SQLite."""

from __future__ import annotations

import json
import sqlite3
from typing import Optional

from recipe_planner.models.shopping_list import ShoppingList


def _row_to_list(row: sqlite3.Row) -> ShoppingList:
    data = dict(row)
    data["categories"] = json.loads(data["categories"])
    data["raw_items"] = json.loads(data["raw_items"])
    data["metadata"] = json.loads(data["metadata"])
    return ShoppingList.from_dict(data)


def save_shopping_list(
    conn: sqlite3.Connection, sl: ShoppingList, meal_plan_id: str | None = None
) -> ShoppingList:
    conn.execute(
        """INSERT OR REPLACE INTO shopping_lists
           (id, meal_plan_id, categories, raw_items, metadata)
           VALUES (?, ?, ?, ?, ?)""",
        (
            sl.id,
            meal_plan_id,
            json.dumps(sl.categories),
            json.dumps(sl.raw_items),
            json.dumps(sl.metadata),
        ),
    )
    return sl


def get_shopping_list(conn: sqlite3.Connection, list_id: str) -> Optional[ShoppingList]:
    cursor = conn.execute("SELECT * FROM shopping_lists WHERE id = ?", (list_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    return _row_to_list(row)


def list_shopping_lists(conn: sqlite3.Connection) -> list[ShoppingList]:
    cursor = conn.execute("SELECT * FROM shopping_lists ORDER BY rowid DESC")
    return [_row_to_list(row) for row in cursor.fetchall()]
