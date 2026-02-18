"""Shopping list data model."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ShoppingList:
    categories: dict[str, list[str]] = field(default_factory=dict)
    raw_items: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.metadata:
            self.metadata = {
                "recipes_included": [],
                "generated_on": datetime.now().strftime("%Y-%m-%d"),
            }

    def to_dict(self) -> dict:
        return {
            "shopping_list": {
                "id": self.id,
                "categories": self.categories,
                "raw_items": self.raw_items,
                "metadata": self.metadata,
            }
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "ShoppingList":
        if "shopping_list" in data:
            data = data["shopping_list"]
        return cls(
            id=data.get("id", ""),
            categories=data.get("categories", {}),
            raw_items=data.get("raw_items", []),
            metadata=data.get("metadata", {}),
        )
