"""Local keyword-based cuisine classification engine."""

from __future__ import annotations

import json
from pathlib import Path

from recipe_planner.models.recipe import Recipe

CUISINE_DATA_PATH = Path(__file__).parent / "cuisine_data.json"

CUISINES = [
    "American", "Italian", "Mexican", "Asian", "Mediterranean",
    "Indian", "Middle Eastern", "African", "Latin American",
    "European", "Other/Fusion",
]


def _load_cuisine_keywords() -> dict[str, list[str]]:
    """Load the cuisine keyword mapping from the JSON data file."""
    if CUISINE_DATA_PATH.exists():
        with open(CUISINE_DATA_PATH) as f:
            return json.load(f)
    return {}


def classify_cuisine(recipe: Recipe) -> str:
    """Classify a recipe's cuisine based on keyword matching.

    Scores the recipe against each cuisine by counting keyword hits
    across ingredients, instructions, title, and tags.
    Returns the highest-scoring cuisine, or 'Other/Fusion' if no strong match.
    """
    keywords_map = _load_cuisine_keywords()
    if not keywords_map:
        return "Other/Fusion"

    # Build a searchable text corpus from the recipe
    text_parts = [recipe.title.lower()]
    for ing in recipe.ingredients:
        text_parts.append(ing.name.lower())
    for step in recipe.instructions:
        text_parts.append(step.lower())
    for tag in recipe.tags:
        text_parts.append(tag.lower())

    corpus = " ".join(text_parts)

    # Score each cuisine
    scores: dict[str, int] = {}
    for cuisine, keywords in keywords_map.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in corpus:
                score += 1
        if score > 0:
            scores[cuisine] = score

    if not scores:
        return "Other/Fusion"

    # Return the highest scoring cuisine
    best = max(scores, key=scores.get)
    return best


def get_cuisine_scores(recipe: Recipe) -> list[tuple[str, int]]:
    """Get ranked cuisine scores for a recipe. Returns list of (cuisine, score)."""
    keywords_map = _load_cuisine_keywords()
    if not keywords_map:
        return [("Other/Fusion", 0)]

    text_parts = [recipe.title.lower()]
    for ing in recipe.ingredients:
        text_parts.append(ing.name.lower())
    for step in recipe.instructions:
        text_parts.append(step.lower())
    for tag in recipe.tags:
        text_parts.append(tag.lower())

    corpus = " ".join(text_parts)

    scores = []
    for cuisine, keywords in keywords_map.items():
        score = sum(1 for kw in keywords if kw.lower() in corpus)
        if score > 0:
            scores.append((cuisine, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores if scores else [("Other/Fusion", 0)]
