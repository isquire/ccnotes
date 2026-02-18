"""Render a shopping list to PDF with checkboxes."""

from __future__ import annotations

from recipe_planner.models.shopping_list import ShoppingList
from recipe_planner.export.pdf_renderer import (
    get_pdf, add_title, add_subtitle, save_pdf,
)


def render_shopping_list_pdf(
    shopping_list: ShoppingList,
    filename: str | None = None,
) -> str:
    """Generate a PDF shopping list with category headers and checkboxes."""
    pdf = get_pdf()

    add_title(pdf, "Shopping List")

    # Metadata
    if shopping_list.metadata.get("generated_on"):
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(
            0, 6,
            f"Generated: {shopping_list.metadata['generated_on']}",
            new_x="LMARGIN", new_y="NEXT",
        )
    if shopping_list.metadata.get("recipes_included"):
        pdf.set_font("Helvetica", "I", 9)
        recipes_str = ", ".join(shopping_list.metadata["recipes_included"])
        pdf.multi_cell(0, 5, f"Recipes: {recipes_str}")

    pdf.ln(4)

    # Categories with items
    for category, items in shopping_list.categories.items():
        add_subtitle(pdf, category)
        pdf.set_font("Helvetica", "", 11)
        for item in items:
            # Checkbox (empty square) + item
            y = pdf.get_y()
            x = pdf.get_x()
            pdf.rect(x + 4, y + 1, 4, 4)  # checkbox
            pdf.cell(12)  # space after checkbox
            pdf.cell(0, 6, item, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # Save
    if not filename:
        filename = "shopping_list.pdf"

    return save_pdf(pdf, filename)
