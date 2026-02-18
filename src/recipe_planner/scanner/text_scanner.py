"""Extract recipe data from plain text using heuristic parsing."""

from __future__ import annotations

import re
from typing import Optional

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe
from recipe_planner.utils.text_helpers import parse_ingredient_string, normalize_whitespace


def extract_recipe_from_text(text: str) -> Recipe:
    """Parse raw text into a Recipe object using heuristic rules."""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    title = _extract_title(lines)
    ingredients_raw, instructions_raw = _split_sections(lines)
    ingredients = _parse_ingredients(ingredients_raw)
    instructions = _parse_instructions(instructions_raw)
    prep_time = _extract_time(text, "prep")
    cook_time = _extract_time(text, "cook")

    confidence_notes = []
    if not title:
        confidence_notes.append("Title could not be determined; using first line")
        title = lines[0] if lines else "Untitled Recipe"
    if not ingredients:
        confidence_notes.append("No ingredients section found")
    if not instructions:
        confidence_notes.append("No instructions section found")

    recipe = Recipe(
        title=title,
        ingredients=ingredients,
        instructions=instructions,
        prep_time=prep_time,
        cook_time=cook_time,
        confidence_notes=confidence_notes,
    )
    return recipe


def _extract_title(lines: list[str]) -> Optional[str]:
    """Extract the recipe title from the text lines."""
    if not lines:
        return None

    # First non-empty line that isn't a section header
    for line in lines:
        lower = line.lower().strip()
        if lower and not any(
            lower.startswith(h)
            for h in ["ingredients", "instructions", "directions", "steps",
                       "method", "prep time", "cook time", "servings",
                       "yield", "notes"]
        ):
            # Remove markdown heading markers
            cleaned = re.sub(r"^#+\s*", "", line).strip()
            if cleaned:
                return cleaned
    return None


def _split_sections(lines: list[str]) -> tuple[list[str], list[str]]:
    """Split text into ingredient lines and instruction lines."""
    ingredient_lines: list[str] = []
    instruction_lines: list[str] = []

    section = None  # 'ingredients', 'instructions', or None

    ingredient_headers = {"ingredients", "ingredient list", "you will need",
                          "what you need", "shopping list"}
    instruction_headers = {"instructions", "directions", "steps", "method",
                           "preparation", "how to make", "procedure"}
    metadata_prefixes = ("prep time", "cook time", "total time", "servings",
                         "yield", "calories", "notes", "source", "author")

    for line in lines:
        lower = line.lower().strip().rstrip(":")
        lower_clean = re.sub(r"^#+\s*", "", lower).strip()

        if lower_clean in ingredient_headers:
            section = "ingredients"
            continue
        elif lower_clean in instruction_headers:
            section = "instructions"
            continue

        # Stop collecting instructions when we hit metadata lines
        if any(lower_clean.startswith(p) for p in metadata_prefixes):
            if section == "instructions":
                section = None
            continue

        if section == "ingredients":
            cleaned = _clean_list_item(line)
            if cleaned:
                ingredient_lines.append(cleaned)
        elif section == "instructions":
            cleaned = _clean_list_item(line)
            if cleaned:
                instruction_lines.append(cleaned)
        elif section is None:
            # Heuristic: lines starting with a bullet/dash/number before a section header
            # might be ingredients if they look like quantities
            cleaned = _clean_list_item(line)
            if cleaned and _looks_like_ingredient(cleaned):
                ingredient_lines.append(cleaned)

    return ingredient_lines, instruction_lines


def _clean_list_item(line: str) -> str:
    """Remove bullet points, numbering, and leading/trailing whitespace."""
    line = line.strip()
    # Remove bullet characters
    line = re.sub(r"^[\-\*\u2022\u2023\u25e6\u2043\u2219]\s*", "", line)
    # Remove numbering like "1.", "1)", "Step 1:"
    line = re.sub(r"^(?:step\s+)?\d+[\.\)\:]\s*", "", line, flags=re.IGNORECASE)
    return line.strip()


def _looks_like_ingredient(line: str) -> bool:
    """Heuristic check if a line looks like an ingredient."""
    # Starts with a number or fraction
    if re.match(r"^\d", line):
        return True
    # Contains common unit words
    units = r"\b(cup|cups|tbsp|tsp|oz|lb|g|kg|ml|l|teaspoon|tablespoon|ounce|pound|clove|can|bunch)\b"
    if re.search(units, line, re.IGNORECASE):
        return True
    return False


def _parse_ingredients(lines: list[str]) -> list[Ingredient]:
    """Parse ingredient lines into Ingredient objects."""
    ingredients = []
    for line in lines:
        parsed = parse_ingredient_string(line)
        ingredients.append(
            Ingredient(
                name=parsed["name"],
                quantity=parsed["quantity"],
                unit=parsed["unit"],
            )
        )
    return ingredients


def _parse_instructions(lines: list[str]) -> list[str]:
    """Parse instruction lines into ordered steps."""
    instructions = []
    for line in lines:
        cleaned = normalize_whitespace(line)
        if cleaned:
            instructions.append(cleaned)
    return instructions


def _extract_time(text: str, time_type: str) -> Optional[str]:
    """Extract prep or cook time from the text."""
    patterns = [
        rf"{time_type}\s*time\s*[:=]?\s*(.+?)(?:\n|$)",
        rf"{time_type}\s*[:=]\s*(.+?)(?:\n|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return normalize_whitespace(match.group(1).strip())
    return None
