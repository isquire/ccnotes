"""Text processing utilities."""

from __future__ import annotations

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text


def title_case(text: str) -> str:
    """Smart title case that doesn't capitalize small words."""
    small_words = {"a", "an", "the", "and", "but", "or", "for", "nor",
                   "in", "on", "at", "to", "of", "by", "with"}
    words = text.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def parse_ingredient_string(text: str) -> dict:
    """Parse an ingredient string like '2 1/2 cups all-purpose flour' into components."""
    text = normalize_whitespace(text)

    # Pattern: optional quantity, optional unit, name
    pattern = r"""
        ^
        (?P<quantity>
            \d+\s+\d+/\d+     # mixed fraction: 1 1/2
            | \d+/\d+          # simple fraction: 1/2
            | \d+\.?\d*        # decimal or integer: 2, 2.5
        )?
        \s*
        (?P<unit>
            tablespoons?|tbsp|teaspoons?|tsp|cups?|ounces?|oz
            |pounds?|lbs?|grams?|g|kilograms?|kg|liters?|l
            |milliliters?|ml|pints?|quarts?|gallons?
            |cloves?|slices?|pieces?|cans?|bunch(?:es)?
            |sprigs?|stalks?|heads?|pinch(?:es)?|dash(?:es)?
            |large|medium|small|whole
        )?
        \s*
        (?P<name>.+)
        $
    """
    match = re.match(pattern, text, re.VERBOSE | re.IGNORECASE)
    if match:
        return {
            "quantity": match.group("quantity") or "",
            "unit": match.group("unit"),
            "name": match.group("name").strip().rstrip(","),
        }
    return {"quantity": "", "unit": None, "name": text}
