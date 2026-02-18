"""Merge duplicate ingredients and sum quantities."""

from __future__ import annotations

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.utils.unit_converter import (
    can_convert,
    convert,
    normalize_unit,
    parse_quantity,
)


def merge_ingredients(ingredients: list[Ingredient]) -> list[Ingredient]:
    """Merge duplicate ingredients by name, summing compatible quantities.

    Groups by normalized name (lowercase, trimmed). When units are
    compatible (both volume or both weight), converts and sums.
    Otherwise, keeps separate entries.
    """
    # Group by normalized name
    groups: dict[str, list[Ingredient]] = {}
    for ing in ingredients:
        key = ing.name.strip().lower()
        groups.setdefault(key, []).append(ing)

    merged: list[Ingredient] = []
    for name_key, group in groups.items():
        if len(group) == 1:
            merged.append(group[0])
            continue

        # Try to merge quantities
        merged_item = _try_merge_group(group)
        merged.append(merged_item)

    return merged


def _try_merge_group(group: list[Ingredient]) -> Ingredient:
    """Attempt to merge a group of same-named ingredients."""
    # Use the first item as the base
    base = group[0]
    base_unit = normalize_unit(base.unit)
    total_qty = parse_quantity(str(base.quantity))

    unmergeable_notes = []

    for ing in group[1:]:
        ing_unit = normalize_unit(ing.unit)
        ing_qty = parse_quantity(str(ing.quantity))

        if base_unit == ing_unit:
            total_qty += ing_qty
        elif base_unit and ing_unit and can_convert(ing_unit, base_unit):
            converted = convert(ing_qty, ing.unit or "", base.unit or "")
            if converted is not None:
                total_qty += converted
            else:
                unmergeable_notes.append(f"+ {ing.display()}")
        elif not base_unit and not ing_unit:
            total_qty += ing_qty
        else:
            unmergeable_notes.append(f"+ {ing.display()}")

    # Format quantity nicely
    if total_qty == int(total_qty):
        qty_str = str(int(total_qty))
    else:
        qty_str = f"{total_qty:.2f}".rstrip("0").rstrip(".")

    notes = base.notes or ""
    if unmergeable_notes:
        notes = (notes + " " + " ".join(unmergeable_notes)).strip()

    return Ingredient(
        name=base.name,
        quantity=qty_str,
        unit=base.unit,
        category=base.category,
        notes=notes if notes else None,
    )
