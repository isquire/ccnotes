"""Render a recipe to PDF."""

from __future__ import annotations

from recipe_planner.models.recipe import Recipe
from recipe_planner.export.pdf_renderer import (
    get_pdf, add_title, add_subtitle, add_metadata_line,
    add_list_item, add_numbered_item, add_horizontal_rule,
    save_pdf,
)
from recipe_planner.utils.text_helpers import slugify


def render_recipe_pdf(recipe: Recipe, filename: str | None = None) -> str:
    """Generate a PDF for a single recipe. Returns the output file path."""
    pdf = get_pdf()

    # Title
    add_title(pdf, recipe.title)

    # Metadata
    if recipe.cuisine:
        add_metadata_line(pdf, "Cuisine", recipe.cuisine)
    if recipe.prep_time:
        add_metadata_line(pdf, "Prep Time", recipe.prep_time)
    if recipe.cook_time:
        add_metadata_line(pdf, "Cook Time", recipe.cook_time)
    if recipe.tags:
        add_metadata_line(pdf, "Tags", ", ".join(recipe.tags))

    pdf.ln(4)
    add_horizontal_rule(pdf)

    # Ingredients
    add_subtitle(pdf, "Ingredients")
    for ing in recipe.ingredients:
        add_list_item(pdf, ing.display())

    pdf.ln(4)
    add_horizontal_rule(pdf)

    # Instructions
    add_subtitle(pdf, "Instructions")
    for i, step in enumerate(recipe.instructions, 1):
        add_numbered_item(pdf, i, step)

    # Save
    if not filename:
        filename = f"recipe_{slugify(recipe.title)}.pdf"

    return save_pdf(pdf, filename)
