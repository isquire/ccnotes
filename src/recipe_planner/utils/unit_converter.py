"""Unit conversion utilities for ingredient normalization."""

from __future__ import annotations

from fractions import Fraction
from typing import Optional

# Volume conversions to milliliters
VOLUME_TO_ML: dict[str, float] = {
    "tsp": 4.929,
    "teaspoon": 4.929,
    "teaspoons": 4.929,
    "tbsp": 14.787,
    "tablespoon": 14.787,
    "tablespoons": 14.787,
    "cup": 236.588,
    "cups": 236.588,
    "fl oz": 29.574,
    "fluid ounce": 29.574,
    "fluid ounces": 29.574,
    "ml": 1.0,
    "milliliter": 1.0,
    "milliliters": 1.0,
    "l": 1000.0,
    "liter": 1000.0,
    "liters": 1000.0,
    "pint": 473.176,
    "pints": 473.176,
    "quart": 946.353,
    "quarts": 946.353,
    "gallon": 3785.41,
    "gallons": 3785.41,
}

# Weight conversions to grams
WEIGHT_TO_G: dict[str, float] = {
    "g": 1.0,
    "gram": 1.0,
    "grams": 1.0,
    "kg": 1000.0,
    "kilogram": 1000.0,
    "kilograms": 1000.0,
    "oz": 28.3495,
    "ounce": 28.3495,
    "ounces": 28.3495,
    "lb": 453.592,
    "lbs": 453.592,
    "pound": 453.592,
    "pounds": 453.592,
}

# Unit normalization map
UNIT_ALIASES: dict[str, str] = {
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "cups": "cup",
    "ounces": "oz",
    "ounce": "oz",
    "pounds": "lb",
    "pound": "lb",
    "lbs": "lb",
    "grams": "g",
    "gram": "g",
    "kilograms": "kg",
    "kilogram": "kg",
    "liters": "l",
    "liter": "l",
    "milliliters": "ml",
    "milliliter": "ml",
    "fluid ounce": "fl oz",
    "fluid ounces": "fl oz",
    "pints": "pint",
    "quarts": "quart",
    "gallons": "gallon",
    "cloves": "clove",
    "slices": "slice",
    "pieces": "piece",
    "cans": "can",
    "bunches": "bunch",
    "sprigs": "sprig",
    "stalks": "stalk",
    "heads": "head",
}


def normalize_unit(unit: str | None) -> str | None:
    """Normalize a unit string to its canonical form."""
    if not unit:
        return None
    unit_lower = unit.strip().lower()
    return UNIT_ALIASES.get(unit_lower, unit_lower)


def parse_quantity(qty_str: str) -> float:
    """Parse a quantity string (supports fractions like '1/2', '1 1/2')."""
    if not qty_str:
        return 0.0
    qty_str = qty_str.strip()

    # Replace unicode fractions
    unicode_fracs = {
        "\u00bc": "1/4", "\u00bd": "1/2", "\u00be": "3/4",
        "\u2153": "1/3", "\u2154": "2/3",
        "\u2155": "1/5", "\u2156": "2/5", "\u2157": "3/5", "\u2158": "4/5",
        "\u2159": "1/6", "\u215a": "5/6",
        "\u215b": "1/8", "\u215c": "3/8", "\u215d": "5/8", "\u215e": "7/8",
    }
    for uf, af in unicode_fracs.items():
        qty_str = qty_str.replace(uf, af)

    try:
        # Handle mixed fractions like "1 1/2"
        parts = qty_str.split()
        if len(parts) == 2 and "/" in parts[1]:
            whole = float(parts[0])
            frac = float(Fraction(parts[1]))
            return whole + frac
        elif "/" in qty_str:
            return float(Fraction(qty_str))
        else:
            return float(qty_str)
    except (ValueError, ZeroDivisionError):
        return 0.0


def can_convert(unit1: str | None, unit2: str | None) -> bool:
    """Check if two units can be converted between each other."""
    u1 = normalize_unit(unit1) or ""
    u2 = normalize_unit(unit2) or ""
    if u1 == u2:
        return True
    both_volume = u1 in VOLUME_TO_ML and u2 in VOLUME_TO_ML
    both_weight = u1 in WEIGHT_TO_G and u2 in WEIGHT_TO_G
    return both_volume or both_weight


def convert(quantity: float, from_unit: str, to_unit: str) -> Optional[float]:
    """Convert a quantity from one unit to another. Returns None if not convertible."""
    fu = normalize_unit(from_unit) or ""
    tu = normalize_unit(to_unit) or ""

    if fu == tu:
        return quantity

    if fu in VOLUME_TO_ML and tu in VOLUME_TO_ML:
        ml = quantity * VOLUME_TO_ML[fu]
        return ml / VOLUME_TO_ML[tu]

    if fu in WEIGHT_TO_G and tu in WEIGHT_TO_G:
        g = quantity * WEIGHT_TO_G[fu]
        return g / WEIGHT_TO_G[tu]

    return None
