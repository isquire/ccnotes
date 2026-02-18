"""Render a meal plan to PDF as a grid/table."""

from __future__ import annotations

from recipe_planner.models.meal_plan import MealPlan
from recipe_planner.export.pdf_renderer import (
    get_pdf, add_title, add_metadata_line, save_pdf,
)


DAY_ORDER = [
    "Saturday", "Sunday", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday", "Next Sunday",
]

MEAL_TYPES = ["breakfast", "lunch", "dinner"]


def render_plan_pdf(plan: MealPlan, filename: str | None = None) -> str:
    """Generate a PDF for a meal plan as a table. Returns the output path."""
    from fpdf import FPDF

    # Use landscape orientation for table
    pdf = FPDF(orientation="L")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Weekly Meal Plan", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"{plan.start_date} to {plan.end_date}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Table dimensions
    col_widths = [25]  # First column (meal type)
    day_col_width = (277 - 25) / len(DAY_ORDER)  # Remaining width / num days
    col_widths.extend([day_col_width] * len(DAY_ORDER))

    row_height = 14

    # Header row
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(col_widths[0], row_height, "Meal", border=1)
    for i, day in enumerate(DAY_ORDER):
        pdf.cell(col_widths[i + 1], row_height, day[:3], border=1, align="C")
    pdf.ln()

    # Data rows
    pdf.set_font("Helvetica", "", 8)
    for meal_type in MEAL_TYPES:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_widths[0], row_height, meal_type.title(), border=1)
        pdf.set_font("Helvetica", "", 8)

        for i, day in enumerate(DAY_ORDER):
            recipe_title = plan.days.get(day, {}).get(meal_type, "-")
            # Truncate long titles to fit cell
            if len(recipe_title) > 20:
                recipe_title = recipe_title[:18] + ".."
            pdf.cell(col_widths[i + 1], row_height, recipe_title, border=1, align="C")
        pdf.ln()

    # Save
    if not filename:
        filename = f"meal_plan_{plan.start_date}.pdf"

    return save_pdf(pdf, filename)
