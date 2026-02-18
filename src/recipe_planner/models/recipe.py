"""Recipe data model with full version tracking support."""

from __future__ import annotations

import copy
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from recipe_planner.models.ingredient import Ingredient


@dataclass
class VersionEntry:
    version: int
    timestamp: str
    changes: list[str]
    snapshot: dict

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "timestamp": self.timestamp,
            "changes": self.changes,
            "snapshot": self.snapshot,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VersionEntry":
        return cls(
            version=data["version"],
            timestamp=data["timestamp"],
            changes=data.get("changes", []),
            snapshot=data.get("snapshot", {}),
        )


@dataclass
class Recipe:
    id: str = ""
    version: int = 1
    title: str = ""
    cuisine: str = ""
    ingredients: list[Ingredient] = field(default_factory=list)
    instructions: list[str] = field(default_factory=list)
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    confidence_notes: list[str] = field(default_factory=list)
    date_added: str = ""
    date_modified: str = ""
    last_used_in_meal_plan: Optional[str] = None
    times_used: int = 0
    original_values: dict = field(default_factory=dict)
    edited_fields: list[str] = field(default_factory=list)
    version_history: list[VersionEntry] = field(default_factory=list)
    change_highlights: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not self.date_added:
            self.date_added = now
        if not self.date_modified:
            self.date_modified = now

    def snapshot(self) -> dict:
        """Return a full snapshot of all editable fields."""
        return {
            "title": self.title,
            "cuisine": self.cuisine,
            "ingredients": [i.to_dict() for i in self.ingredients],
            "instructions": list(self.instructions),
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "tags": list(self.tags),
        }

    def to_dict(self) -> dict:
        return {
            "recipe": {
                "id": self.id,
                "version": self.version,
                "title": self.title,
                "cuisine": self.cuisine,
                "ingredients": [i.to_dict() for i in self.ingredients],
                "instructions": self.instructions,
                "prep_time": self.prep_time,
                "cook_time": self.cook_time,
                "tags": self.tags,
                "confidence_notes": self.confidence_notes,
                "date_added": self.date_added,
                "date_modified": self.date_modified,
                "last_used_in_meal_plan": self.last_used_in_meal_plan,
                "times_used": self.times_used,
                "original_values": self.original_values,
                "edited_fields": self.edited_fields,
                "version_history": [v.to_dict() for v in self.version_history],
                "change_highlights": self.change_highlights,
            }
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def initialize_original_values(self) -> None:
        """Store original values on first creation. Must be called once."""
        if not self.original_values:
            self.original_values = {
                "title": self.title,
                "cuisine": self.cuisine,
                "ingredients": [i.to_dict() for i in self.ingredients],
                "instructions": list(self.instructions),
                "prep_time": self.prep_time,
                "cook_time": self.cook_time,
                "tags": list(self.tags),
            }

    def add_version_history_entry(self, changes: list[str] | None = None) -> None:
        """Append a version history entry with the current snapshot."""
        entry = VersionEntry(
            version=self.version,
            timestamp=self.date_modified,
            changes=changes or [],
            snapshot=self.snapshot(),
        )
        self.version_history.append(entry)

    @classmethod
    def from_dict(cls, data: dict) -> "Recipe":
        """Create Recipe from a dict. Accepts either {'recipe': {...}} or flat dict."""
        if "recipe" in data:
            data = data["recipe"]
        ingredients = [Ingredient.from_dict(i) for i in data.get("ingredients", [])]
        version_history = [
            VersionEntry.from_dict(v) for v in data.get("version_history", [])
        ]
        return cls(
            id=data.get("id", ""),
            version=data.get("version", 1),
            title=data.get("title", ""),
            cuisine=data.get("cuisine", ""),
            ingredients=ingredients,
            instructions=data.get("instructions", []),
            prep_time=data.get("prep_time"),
            cook_time=data.get("cook_time"),
            tags=data.get("tags", []),
            confidence_notes=data.get("confidence_notes", []),
            date_added=data.get("date_added", ""),
            date_modified=data.get("date_modified", ""),
            last_used_in_meal_plan=data.get("last_used_in_meal_plan"),
            times_used=data.get("times_used", 0),
            original_values=data.get("original_values", {}),
            edited_fields=data.get("edited_fields", []),
            version_history=version_history,
            change_highlights=data.get("change_highlights", {}),
        )
