"""Ingredient data model."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Ingredient:
    name: str
    quantity: str | float | int
    unit: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"name": self.name, "quantity": self.quantity, "unit": self.unit}
        if self.category:
            d["category"] = self.category
        if self.notes:
            d["notes"] = self.notes
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return cls(
            name=data["name"],
            quantity=data.get("quantity", ""),
            unit=data.get("unit"),
            category=data.get("category"),
            notes=data.get("notes"),
        )

    def display(self) -> str:
        parts = []
        if self.quantity:
            parts.append(str(self.quantity))
        if self.unit:
            parts.append(self.unit)
        parts.append(self.name)
        return " ".join(parts)
