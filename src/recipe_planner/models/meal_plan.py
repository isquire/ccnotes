"""Meal plan data model."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MealPlan:
    start_date: str = ""
    end_date: str = ""
    days: dict[str, dict[str, str]] = field(default_factory=dict)
    recipes_used: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.metadata:
            self.metadata = {
                "generated_on": datetime.now().strftime("%Y-%m-%d"),
                "notes": [],
            }

    def to_dict(self) -> dict:
        return {
            "meal_plan": {
                "id": self.id,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "days": self.days,
                "recipes_used": self.recipes_used,
                "metadata": self.metadata,
            }
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "MealPlan":
        if "meal_plan" in data:
            data = data["meal_plan"]
        return cls(
            id=data.get("id", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            days=data.get("days", {}),
            recipes_used=data.get("recipes_used", []),
            metadata=data.get("metadata", {}),
        )
